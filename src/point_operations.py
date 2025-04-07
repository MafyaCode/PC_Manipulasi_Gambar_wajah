# src/point_operations.py

import cv2
import numpy as np

def adjust_brightness(image, value):
    """Menyesuaikan kecerahan citra."""
    if value == 0:
        return image # Tidak ada perubahan

    if len(image.shape) == 2: # Jika sudah grayscale
        print("Info: Penyesuaian kecerahan pada citra grayscale menggunakan metode add/subtract.")
        adjusted = np.clip(image.astype(np.int16) + value, 0, 255).astype(np.uint8)
        return adjusted
    elif len(image.shape) == 3 and image.shape[2] == 3: # Jika BGR
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        # Tambah/kurang nilai kecerahan ke channel V (Value)
        # Gunakan np.int16 untuk perhitungan sementara agar tidak wrap around 0-255
        v_adjusted = np.clip(v.astype(np.int16) + value, 0, 255).astype(np.uint8)
        final_hsv = cv2.merge((h, s, v_adjusted))
        bright_image = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        return bright_image
    else:
        print(f"Error: Format citra tidak didukung untuk brightness (shape: {image.shape})")
        return image # Kembalikan original jika format aneh

def adjust_contrast(image, value):
    """Menyesuaikan kontras citra."""
    if value == 0:
        return image # Tidak ada perubahan

    # Rumus penyesuaian kontras
    # alpha > 1: increase contrast, 0 < alpha < 1: decrease contrast
    # Pastikan pembagi tidak nol jika value = 131 atau -127 (jarang terjadi tapi untuk keamanan)
    if value >= 131: value = 130
    if value <= -127: value = -126

    alpha = float(131 * (value + 127)) / (127 * (131 - value))
    # Beta (brightness control) kita set berdasarkan alpha agar titik tengah (127) tidak berubah
    gamma = 127 * (1 - alpha)

    # Terapkan penyesuaian kontras
    contrast_image = cv2.addWeighted(image, alpha, image, 0, gamma)
    # Pastikan nilai tetap dalam rentang 0-255 dan tipe data uint8
    contrast_image = np.clip(contrast_image, 0, 255).astype(np.uint8)
    return contrast_image

def image_negative(image):
    """Membuat citra negatif."""
    return cv2.bitwise_not(image)

def apply_threshold(image, threshold_value, threshold_type='binary'):
    """Menerapkan thresholding pada citra (akan dikonversi ke grayscale jika perlu)."""
    if len(image.shape) == 3 and image.shape[2] == 3: # Cek jika citra berwarna (BGR)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif len(image.shape) == 2: # Jika sudah grayscale
        gray_image = image
    else:
        print(f"Error: Format citra tidak didukung untuk thresholding (shape: {image.shape})")
        return image # Kembalikan original

    # Pilih tipe thresholding
    if threshold_type.lower() == 'binary':
        thresh_mode = cv2.THRESH_BINARY
    elif threshold_type.lower() == 'binary_inv':
        thresh_mode = cv2.THRESH_BINARY_INV
    # Tambahkan tipe lain jika perlu (THRESH_TRUNC, THRESH_TOZERO, etc.)
    else:
         print(f"Warning: Tipe threshold '{threshold_type}' tidak dikenal, menggunakan 'binary'.")
         thresh_mode = cv2.THRESH_BINARY

    # Terapkan thresholding
    ret, threshold_image = cv2.threshold(gray_image, threshold_value, 255, thresh_mode)
    return threshold_image

def to_grayscale(image, method='opencv'):
    """Mengkonversi citra berwarna menjadi grayscale."""
    # Cek jika citra sudah grayscale
    if len(image.shape) == 2:
        print("Info: Citra input sudah grayscale.")
        return image
    elif len(image.shape) != 3 or image.shape[2] != 3: # Pastikan ini citra 3 channel (BGR)
         print(f"Error: Format citra input tidak didukung untuk konversi grayscale (shape: {image.shape})")
         return None # Kembalikan None jika bukan citra BGR

    # Lakukan konversi berdasarkan metode
    gray_image = None
    method_lower = method.lower()
    if method_lower == 'opencv':
        print("Info: Konversi ke grayscale menggunakan metode OpenCV (cvtColor).")
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif method_lower == 'numpy':
        print("Info: Konversi ke grayscale menggunakan metode NumPy (rata-rata).")
        # Pastikan tipe data float untuk mean, lalu konversi ke uint8
        gray_image = np.mean(image.astype(np.float32), axis=2).astype(np.uint8)
    else:
        print(f"Error: Metode '{method}' tidak dikenal. Gunakan 'opencv' atau 'numpy'.")
        # Tidak return None agar main.py bisa handle, kembalikan citra asli
        return image

    return gray_image