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

## Cara Pengunaan
1. Siapkan 4 titik patokan (misal: stiker warna terang) di 4 sudut meja kerja Anda membentuk persegi panjang.
2. Ukur jarak asli antar titik tersebut menggunakan meteran.
3. Buka file config.py, lalu ubah nilai REAL_WIDTH_CM dan REAL_HEIGHT_CM sesuai dengan hasil pengukuran Anda.
4. Jalankan aplikasi: python main.py
5. Klik **"Buka Foto"**, pilih foto meja yang ada mal-nya.
6. Klik tepat pada 4 titik patokan di layar (urutan: Kiri-Atas, Kanan-Atas, Kanan-Bawah, Kiri-Bawah).
7. Aplikasi otomatis akan meluruskan gambar dan menampilkan ukuran panjang x lebar mal Anda.

## Struktur Direktori
- `main.py`: Antarmuka grafis (GUI) utama aplikasi.
- `config.py`: Tempat mengatur ukuran asli meja dan pengaturan lainnya.
- `utils/transform.py`: Algoritma AI untuk mengoreksi kemiringan (Warp Perspective).
