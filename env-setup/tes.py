import sys

def verify_libraries():
    """
    Fungsi untuk memeriksa instalasi dan versi dari library-library penting.
    """
    # Daftar library yang ingin diperiksa.
    required_libraries = [
        'librosa',
        'soundfile',
        'scipy',
        'cv2',
        'skimage',
        'matplotlib',
        'moviepy',
        'jupyter',
        'numpy',
        'pandas'
    ]
    
    print("--- Memulai Verifikasi Instalasi Library ---")
    print(f"Versi Python yang digunakan: {sys.version}\n")
    
    all_installed = True
    
    for lib_name in required_libraries:
        try:
            lib = __import__(lib_name)
            
            try:
                version = lib.__version__
            except AttributeError:
                version = " "
            
            print(f"[ ✓ ] {lib_name.ljust(15)}: Terinstall ({version})")
            
        except ImportError:
            print(f"[ X ] {lib_name.ljust(15)}: TIDAK TERINSTALL")
            all_installed = False

if __name__ == "__main__":
    verify_libraries()