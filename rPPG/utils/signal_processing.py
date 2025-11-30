import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision as mp_vision
import scipy.signal as signal
import os

def extract_rppg_signal(frame, roi):
    x, y, w, h = roi
    if w > 0 and h > 0:
        roi_frame = frame[y:y+h, x:x+w]
        # Calculate mean of each channel (B, G, R)
        means = cv2.mean(roi_frame)
        b_mean, g_mean, r_mean = means[0], means[1], means[2]
        
        # Green Chromaticity Normalization: G / (R + G + B)
        # Adds robustness to lighting intensity changes
        total_intensity = r_mean + g_mean + b_mean
        if total_intensity == 0:
            return 0.0
            
        normalized_green = g_mean / total_intensity
        return normalized_green
    return None

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs # Frekuensi Nyquist
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], btype='band')
    return b, a

def calculate_rate_from_fft(signal_values, fs, lowcut_hz, highcut_hz):
    if len(signal_values) < 20: # Membutuhkan panjang sinyal yang cukup untuk analisis FFT
        return 0

    N = len(signal_values)
    yf = np.fft.fft(signal_values)
    xf = np.fft.fftfreq(N, 1 / fs)

    # Ambil hanya spektrum positif dan normalisasi amplitudo
    xf_positive = xf[:N//2]
    yf_positive = 2.0/N * np.abs(yf[0:N//2])

    # Cari indeks frekuensi dalam rentang yang valid
    valid_indices = np.where((xf_positive >= lowcut_hz) & (xf_positive <= highcut_hz))[0]

    if len(valid_indices) == 0: # Tidak ada frekuensi dalam rentang valid
        return 0

    valid_yf = yf_positive[valid_indices]
    valid_xf = xf_positive[valid_indices]

    if len(valid_yf) == 0: # Pengecekan tambahan
        return 0

    # Temukan frekuensi dengan amplitudo terbesar (puncak dominan)
    dominant_peak_index_in_valid = np.argmax(valid_yf)
    dominant_frequency_hz = valid_xf[dominant_peak_index_in_valid]

    rate_per_minute = dominant_frequency_hz * 60 # Konversi Hz ke per menit
    return rate_per_minute


class HealthAnalyzer:
    def __init__(self, face_model_path="models/blaze_face_short_range.tflite",
                 fps=30,
                 rppg_lowcut=0.67, rppg_highcut=4.0,
                 min_signal_length_factor=2,
                 frame_buffer_factor=10):
        self.fps = fps
        self.min_signal_length = int(min_signal_length_factor * self.fps)
        self.frame_buffer_limit = int(frame_buffer_factor * self.fps)

        self.rppg_lowcut = rppg_lowcut
        self.rppg_highcut = rppg_highcut

        self.face_detector = None
        self._load_models(face_model_path) # Muat model MediaPipe

        # Desain koefisien filter untuk rPPG
        self.rppg_b, self.rppg_a = butter_bandpass(self.rppg_lowcut, self.rppg_highcut, self.fps)

        # Buffer untuk menyimpan sinyal mentah yang diekstrak
        self.rppg_signal_buffer = []

    def _load_models(self, face_model_path):
        try:
            # Inisialisasi FaceDetector
            if not os.path.exists(face_model_path):
                raise FileNotFoundError(f"File model wajah tidak ditemukan: {face_model_path}")
            face_base_options = mp_python.BaseOptions(model_asset_path=face_model_path)
            face_options = mp_vision.FaceDetectorOptions(
                base_options=face_base_options,
                running_mode=mp_vision.RunningMode.IMAGE,
                min_detection_confidence=0.5
            )
            self.face_detector = mp_vision.FaceDetector.create_from_options(face_options)

            print("Model MediaPipe di HealthAnalyzer berhasil dimuat.")
        except Exception as e:
            print(f"Error saat memuat model MediaPipe di HealthAnalyzer: {e}")
            raise e

    def detect_faces(self, mp_image):
        if self.face_detector:
            try:
                return self.face_detector.detect(mp_image)
            except Exception as e:
                print(f"Error deteksi wajah: {e}")
        return None

    def process_rppg_from_face(self, frame_for_signal, face_detection_result):
        if face_detection_result is None or not face_detection_result.detections:
            return None

        # Dapatkan bounding box utama wajah
        detection = face_detection_result.detections[0]
        bbox = detection.bounding_box
        frame_h, frame_w, _ = frame_for_signal.shape
        x, y, w, h = int(bbox.origin_x), int(bbox.origin_y), int(bbox.width), int(bbox.height)

        # Validasi bounding box utama
        x = max(0, min(x, frame_w - 1))
        y = max(0, min(y, frame_h - 1))
        w = max(0, min(w, frame_w - x))
        h = max(0, min(h, frame_h - y))

        if not (w > 0 and h > 0):
            return None

        extracted_signals = [] 
        # Definisi, validasi, ekstraksi, dan penggambaran untuk ROI Dahi
        fh_x, fh_y, fh_w, fh_h = int(x+w*0.25), int(y+h*(-0.1)), int(w*0.5), int(h*0.20)
        fh_x,fh_y = max(0,min(fh_x,frame_w-1)),max(0,min(fh_y,frame_h-1))
        fh_w,fh_h = max(0,min(fh_w,frame_w-fh_x)),max(0,min(fh_h,frame_h-fh_y))
        if fh_w > 0 and fh_h > 0:
            val = extract_rppg_signal(frame_for_signal, (fh_x, fh_y, fh_w, fh_h))
            if val is not None: extracted_signals.append(val)
            cv2.rectangle(frame_for_signal, (fh_x, fh_y), (fh_x + fh_w, fh_y + fh_h), (0, 255, 255), 1) # Cyan

        if extracted_signals:
            rppg_value = np.mean(extracted_signals)
            self.rppg_signal_buffer.append(rppg_value)
            if len(self.rppg_signal_buffer) > self.frame_buffer_limit:
                self.rppg_signal_buffer.pop(0)
            return rppg_value
        return None

    def filter_and_calculate_hr(self):
        if len(self.rppg_signal_buffer) < self.min_signal_length:
            return list(self.rppg_signal_buffer), 0.0 # Kembalikan buffer mentah jika terlalu pendek
        try:
            # Tentukan panjang padding untuk filtfilt, hindari error jika sinyal terlalu pendek
            padlen = min(self.min_signal_length -1, len(self.rppg_signal_buffer)-1)
            
            # Standardization: (Signal - Mean) / StdDev
            # Adds robustness to amplitude variations (e.g. motion artifacts)
            signal_array = np.array(self.rppg_signal_buffer)
            if np.std(signal_array) > 1e-6: # Avoid division by zero
                standardized_signal = (signal_array - np.mean(signal_array)) / np.std(signal_array)
                signal_to_filter = standardized_signal.tolist()
            else:
                signal_to_filter = self.rppg_signal_buffer

            if padlen <=0: # Tidak cukup data untuk filtfilt yang stabil
                 filtered_signal = list(signal_to_filter)
            else:
                 filtered_signal = signal.filtfilt(self.rppg_b, self.rppg_a, signal_to_filter, padlen=padlen).tolist()

            hr = calculate_rate_from_fft(filtered_signal, self.fps, self.rppg_lowcut, self.rppg_highcut)
            return filtered_signal, hr
        except ValueError: # Jika terjadi error saat filtering/FFT
            return list(self.rppg_signal_buffer), 0.0

    def clear_buffers(self):
        self.rppg_signal_buffer.clear()

    def has_models(self):
        return self.face_detector is not None