# ==========================================
# PENGATURAN KALIBRASI UKURAN MEJA FISIK
# ==========================================

# Masukkan jarak asli antar 4 titik patokan di meja Anda (dalam Centimeter)
# Misalnya: Titik kiri atas ke kanan atas adalah 150 cm.
REAL_WIDTH_CM = 150.0  

# Misalnya: Titik kiri atas ke kiri bawah adalah 100 cm.
REAL_HEIGHT_CM = 100.0  

# ==========================================
# PENGATURAN DETEKSI AI (OpenCV Parameters)
# ==========================================
BLUR_KERNEL = 5          # Tingkat kehalusan (untuk menghilangkan noise tekstur kayu)
CANNY_THRESHOLD_1 = 50   # Batas bawah deteksi tepi
CANNY_THRESHOLD_2 = 150  # Batas atas deteksi tepi
MIN_AREA_CONTOUR = 5000  # Abaikan debu/benda kecil (dalam pixel)
