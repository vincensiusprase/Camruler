import numpy as np
import cv2

def order_points(pts):
    """
    Mengurutkan 4 titik yang diklik user menjadi urutan baku:
    [Kiri-Atas, Kanan-Atas, Kanan-Bawah, Kiri-Bawah]
    """
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]      # Top-Left
    rect[2] = pts[np.argmax(s)]      # Bottom-Right
    
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]   # Top-Right
    rect[3] = pts[np.argmax(diff)]   # Bottom-Left
    return rect

def four_point_transform(image, pts):
    """
    Melakukan 'Warping' atau meluruskan gambar miring menjadi tampak atas tegak lurus
    berdasarkan 4 titik kordinat patokan.
    """
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    # Hitung lebar maksimum gambar baru
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    # Hitung tinggi maksimum gambar baru
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    # Titik tujuan untuk gambar yang sudah lurus
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    # Kalkulasi matrix transformasi dan terapkan pada gambar
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    return warped
