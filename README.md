# Repositori Tugas
# Kelas Sistem & Tekonologi  Multimedia (IF25-40305)

<p align="center">
    <img src="logo/IF4021_logo.png" width="300">
</p>

Repositori ini berisi kumpulan *file* dan *notebook* Jupyter yang berkaitan dengan mata kuliah Sistem Teknologi Multimedia. Proyek ini mencakup latihan dan tugas-tugas terkait.

---

## Struktur Repositori

Berikut adalah struktur dari repositori ini:

* **`Excercise 1/`**: Direktori ini berisi Tugas Multimedia Data Representation.
    * **`3_exercise_loading_media.ipynb`**: *Notebook* Jupyter untuk memuat dan memanipulasi *file* media.
    * **`data/`**: Direktori yang berisi *file* media untuk latihan.
        * **`whale_sound.wav`**: *file* audio suara paus.

* **`env-setup/`**: Berisi Tugas Environment Setup.
    * **`122140008.pdf`**: File laporan tugas environment setup
    * **`tes.py`**: *Script* Python untuk pengujian.
    * **`test_multimedia.py`**: *Script* Python untuk pengujian multimedia.
    * **`sine_wave_test.png`**: Gambar untuk pengujian
    * **`test_image.png`**: Gambar untuk pengujian.

* **`ho-audio/`**: Direktori ini berisi Hands-on Pemrosesan Audio.
    * **`122140008_audio_processing_report.pdf`**: Laporan pemrosesan audio.
    * **`HO_AudioProcessing_122140008.ipynb`**: *Notebook* Jupyter utama untuk tugas pemrosesan audio.
    * **`media/`**: Berisi *file* audio yang digunakan dan dihasilkan dalam tugas.
        * **`1_resampled.wav`**: *File* audio yang telah di-*resample*.
        * **`2_bandpass.wav`, `2_highpass.wav`, `2_lowpass.wav`**: *File* audio hasil dari berbagai jenis *filter*.
        * **`3_pitch_shifted_12.wav`, `3_pitch_shifted_7.wav`**: *File* audio dengan *pitch* yang telah diubah.
        * **`3_combined_audio.wav`**: Merupakan gabungan dari *file* audio `3_pitch_shifted_12.wav` dan  `3_pitch_shifted_7.wav`.
        * **`4_processed_audio.wav`, `4_processed_normalized_audio.wav`**: *File* audio yang telah diproses dan dinormalisasi.
        * **`5_remixed_song.wav`**: Lagu yang telah di-*remix*.
        * **`Multimedia_1.wav`, `Multimedia_2.1.wav`**: *File* audio sumber.

---

## Cara Menjalankan Kode

Untuk menjalankan kode dalam repositori ini, Anda perlu memiliki Python dan Jupyter Notebook yang terinstal. Ikuti langkah-langkah di bawah ini:

1.  **Instal Ketergantungan**: Pastikan Anda telah menginstal semua pustaka Python yang diperlukan. Anda dapat menginstalnya menggunakan `pip`:

    ```bash
    pip install numpy matplotlib scipy librosa jupyterlab
    ```

2.  **Jalankan Jupyter Notebook**: Untuk menjalankan *file* `.ipynb`, navigasikan ke direktori repositori melalui terminal dan jalankan perintah berikut:

    ```bash
    jupyter notebook
    ```

    Setelah itu, buka *file notebook* yang ingin Anda jalankan (misalnya, `3_exercise_loading_media.ipynb` atau `HO_AudioProcessing_122140008.ipynb`) dari antarmuka Jupyter di *browser* Anda.

3.  **Jalankan Script Python**: Untuk menjalankan *file* `.py`, gunakan perintah `python` di terminal:
    ```bash
    python "env-setup/tes.py"
    ```
    atau
    ```bash
    python "env-setup/test_multimedia.py"
    ```