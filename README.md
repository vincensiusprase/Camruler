# AutoMeasure AI - Pengukur Mal Kaca & Triplek

Aplikasi berbasis *Computer Vision* (OpenCV) untuk mengukur dimensi (panjang dan lebar) mal kardus atau triplek secara presisi. Aplikasi ini menggunakan metode **4-Point Perspective Transform** untuk menghilangkan distorsi kamera dan menghitung ukuran asli dalam sentimeter (cm).

## Fitur Utama
- **Koreksi Perspektif:** Menghitung ukuran akurat meskipun kamera dipasang sedikit miring.
- **Deteksi Otomatis:** Otomatis mencari tepi (kontur) mal kardus/triplek di atas meja.
- **GUI Sederhana:** Antarmuka Tkinter yang mudah digunakan oleh operator bengkel.

## Prasyarat Instalasi
Pastikan Anda sudah menginstal Python (disarankan versi 3.8 - 3.11).

1. Clone atau download repositori ini.
2. Buka terminal / command prompt di folder proyek ini.
3. Instal library yang dibutuhkan dengan perintah:
   ```bash
   pip install -r requirements.txt
