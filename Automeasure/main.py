import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

# Import fungsi custom
import config
from utils.transform import four_point_transform

class AutoMeasureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoMeasure AI - Sistem Pengukur Mal Kaca")
        self.root.geometry("1100x800")
        self.root.configure(bg="#2c3e50")

        self.points = []
        self.img_original = None
        self.ratio_display = 1.0

        # ---- HEADER UI ----
        self.frame_header = tk.Frame(root, bg="#34495e", pady=10)
        self.frame_header.pack(fill=tk.X)

        self.btn_load = tk.Button(self.frame_header, text="📷 Buka Foto Meja", command=self.load_image, 
                                  bg="#3498db", fg="white", font=("Arial", 12, "bold"))
        self.btn_load.pack(side=tk.LEFT, padx=20)

        self.btn_reset = tk.Button(self.frame_header, text="🔄 Reset Titik", command=self.reset_points, 
                                   bg="#e74c3c", fg="white", font=("Arial", 12, "bold"))
        self.btn_reset.pack(side=tk.LEFT, padx=10)

        self.lbl_status = tk.Label(self.frame_header, text="Status: Menunggu foto...", 
                                   bg="#34495e", fg="#2ecc71", font=("Arial", 12))
        self.lbl_status.pack(side=tk.RIGHT, padx=20)

        # ---- CANVAS GAMBAR ----
        self.canvas_frame = tk.Frame(root, bg="#2c3e50")
        self.canvas_frame.pack(pady=20)

        self.canvas = tk.Canvas(self.canvas_frame, bg="black", width=800, height=500, cursor="crosshair")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)

        # ---- PANEL HASIL ----
        self.lbl_result = tk.Label(root, text="Panjang: - cm | Lebar: - cm", 
                                   font=("Arial", 24, "bold"), bg="#2c3e50", fg="#f1c40f")
        self.lbl_result.pack(pady=10)

    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
        if path:
            self.img_original = cv2.imread(path)
            self.reset_points()
            self.lbl_status.config(text="Status: Klik 4 sudut titik patokan di gambar!")

    def reset_points(self):
        self.points = []
        self.lbl_result.config(text="Panjang: - cm | Lebar: - cm")
        self.display_image()

    def display_image(self):
        if self.img_original is None: return
        h, w = self.img_original.shape[:2]
        
        # Sesuaikan gambar agar muat di canvas GUI
        self.ratio_display = min(800/w, 500/h)
        new_size = (int(w * self.ratio_display), int(h * self.ratio_display))
        img_res = cv2.resize(self.img_original, new_size)
        
        img_rgb = cv2.cvtColor(img_res, cv2.COLOR_BGR2RGB)
        self.img_tk = ImageTk.PhotoImage(Image.fromarray(img_rgb))
        
        self.canvas.config(width=new_size[0], height=new_size[1])
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img_tk)

    def on_click(self, event):
        if self.img_original is None:
            messagebox.showwarning("Peringatan", "Buka foto terlebih dahulu!")
            return
        if len(self.points) >= 4:
            return

        # Simpan koordinat asli (sebelum di-resize ke GUI)
        real_x = int(event.x / self.ratio_display)
        real_y = int(event.y / self.ratio_display)
        self.points.append([real_x, real_y])

        # Gambar titik merah di canvas
        self.canvas.create_oval(event.x-4, event.y-4, event.x+4, event.y+4, fill="red", outline="white")
        self.lbl_status.config(text=f"Status: {len(self.points)}/4 Titik dipilih")

        if len(self.points) == 4:
            self.lbl_status.config(text="Status: Sedang memproses AI...")
            self.process_measurement()

    def process_measurement(self):
        pts = np.array(self.points, dtype="float32")
        
        # 1. Luruskan gambar (Perspective Transform)
        warped = four_point_transform(self.img_original, pts)
        
        # 2. Hitung Rasio Pixel ke CM berdasarkan config.py
        h_pixel, w_pixel = warped.shape[:2]
        ratio_w = config.REAL_WIDTH_CM / w_pixel
        ratio_h = config.REAL_HEIGHT_CM / h_pixel

        # 3. Pengolahan Gambar untuk mencari Mal (Kardus/Triplek)
        gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (config.BLUR_KERNEL, config.BLUR_KERNEL), 0)
        edged = cv2.Canny(blur, config.CANNY_THRESHOLD_1, config.CANNY_THRESHOLD_2)
        
        # Operasi morfologi untuk menutup lubang/garis putus pada kontur
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)

        # Temukan kontur
        cnts, _ = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(cnts) == 0:
            messagebox.showerror("Gagal", "Mal tidak terdeteksi! Coba perbaiki pencahayaan.")
            self.lbl_status.config(text="Status: Gagal mendeteksi mal.")
            return

        # Cari kontur paling besar (diasumsikan sebagai mal)
        c = max(cnts, key=cv2.contourArea)

        if cv2.contourArea(c) < config.MIN_AREA_CONTOUR:
            messagebox.showwarning("Peringatan", "Objek terlalu kecil, pastikan area bersih dari kotoran.")
            return

        # 4. Ambil Bounding Box Lurus
        x, y, w, h = cv2.boundingRect(c)

        # 5. Konversi Pixel ke Centimeter
        panjang_cm = h * ratio_h
        lebar_cm = w * ratio_w

        # Jika orientasi mendatar (lebar > panjang), kita swap agar penyebutannya logis
        if lebar_cm > panjang_cm:
            panjang_cm, lebar_cm = lebar_cm, panjang_cm

        # Tampilkan Hasil di GUI
        self.lbl_result.config(text=f"Panjang: {panjang_cm:.1f} cm  |  Lebar: {lebar_cm:.1f} cm")
        self.lbl_status.config(text="Status: Pengukuran Selesai!")

        # 6. Gambar kotak hijau hasil deteksi ke window baru untuk validasi
        cv2.rectangle(warped, (x, y), (x + w, y + h), (0, 255, 0), 3)
        cv2.putText(warped, f"{lebar_cm:.1f}cm x {panjang_cm:.1f}cm", (x, y - 15), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
        
        # Ubah ukuran window preview agar pas di layar
        warped_resized = cv2.resize(warped, (800, 600))
        cv2.imshow("Preview Hasil Deteksi (Tekan SPACE/ENTER untuk menutup)", warped_resized)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoMeasureApp(root)
    root.mainloop()
