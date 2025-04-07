# src/main.py

import cv2
import argparse  # Library standar Python untuk memproses argumen command line
import os        # Library standar Python untuk interaksi dengan sistem operasi (path, folder)
import sys       # Library standar Python untuk interaksi sistem (keluar program)

# Coba impor semua fungsi dari file point_operations.py
try:
    from point_operations import (adjust_brightness, adjust_contrast,
                                  image_negative, apply_threshold, to_grayscale)
except ImportError:
    print("CRITICAL ERROR: Tidak dapat menemukan file 'point_operations.py'.")
    print("Pastikan file tersebut ada di dalam folder 'src/' dan tidak ada error di dalamnya.")
    sys.exit(1) # Keluar dari program jika import gagal

def main():
    # --- Setup Argumen Parser ---
    # Membuat objek parser untuk mendefinisikan argumen yang bisa diterima program
    parser = argparse.ArgumentParser(
        description="Program untuk melakukan Operasi Titik (Intensitas) pada Citra.",
        formatter_class=argparse.RawTextHelpFormatter # Agar deskripsi help tampil lebih rapi
        )

    # Menambahkan argumen-argumen yang dibutuhkan
    parser.add_argument("-i", "--input", required=True, help="Path lengkap ke file citra input.")
    parser.add_argument("-o", "--output_dir", required=True, help="Path ke folder tujuan untuk menyimpan hasil.")
    parser.add_argument(
        "-op", "--operation", required=True,
        choices=['brightness', 'contrast', 'negative', 'threshold', 'grayscale'],
        help="Jenis operasi titik yang akan dilakukan:\n"
             "- brightness: Ubah kecerahan (butuh -v)\n"
             "- contrast: Ubah kontras (butuh -v)\n"
             "- negative: Buat citra negatif\n"
             "- threshold: Buat citra hitam/putih (butuh -v)\n"
             "- grayscale: Ubah ke skala abu-abu (opsional -m)"
        )
    parser.add_argument(
        "-v", "--value", type=int, default=None, # Defaultnya None jika tidak diberikan
        help="Nilai integer untuk operasi (wajib untuk brightness, contrast, threshold)."
        )
    parser.add_argument(
        "-m", "--method", default='opencv', choices=['opencv', 'numpy'],
        help="Metode yang digunakan untuk operasi 'grayscale'. Pilihan: 'opencv' (default), 'numpy'."
        )

    # Memproses argumen yang diberikan pengguna saat menjalankan script
    args = parser.parse_args()

    # --- Validasi Input Pengguna ---
    # Cek apakah file input ada
    if not os.path.isfile(args.input): # Lebih spesifik cek file
        print(f"Error: File input tidak ditemukan atau bukan file: {args.input}")
        return # Hentikan eksekusi fungsi main

    # Cek (dan buat jika perlu) folder output
    if not os.path.exists(args.output_dir):
        print(f"Info: Folder output tidak ditemukan. Membuat folder di: {args.output_dir}")
        try:
            os.makedirs(args.output_dir)
        except OSError as e:
            print(f"Error: Gagal membuat folder output: {e}")
            return
    elif not os.path.isdir(args.output_dir):
         print(f"Error: Path output yang diberikan bukanlah sebuah folder: {args.output_dir}")
         return


    # Validasi apakah --value diberikan untuk operasi yang memerlukannya
    needs_value = ['brightness', 'contrast', 'threshold']
    if args.operation in needs_value and args.value is None:
        print(f"Error: Operasi '{args.operation}' membutuhkan argumen --value (-v).")
        print("Contoh: -op brightness -v 50")
        return

    # Validasi rentang nilai untuk operasi tertentu (opsional tapi bagus)
    if args.operation == 'threshold' and args.value is not None:
        if not (0 <= args.value <= 255):
             print(f"Error: Nilai threshold (-v) harus antara 0 dan 255. Diberikan: {args.value}")
             return
    # (Tambahkan validasi rentang lain jika perlu, misal untuk brightness/contrast)


    # --- Memuat Citra ---
    print(f"Info: Memuat citra dari {args.input}...")
    # Coba baca berwarna dulu. IMREAD_UNCHANGED bisa handle alpha channel jika ada.
    image = cv2.imread(args.input, cv2.IMREAD_UNCHANGED)

    if image is None:
        print(f"Error: Gagal memuat citra dari {args.input} menggunakan OpenCV. Pastikan file gambar valid.")
        return

    # Simpan shape asli untuk referensi
    original_shape = image.shape
    print(f"Info: Citra dimuat dengan ukuran {original_shape[1]}x{original_shape[0]} piksel, Channels: {len(original_shape) > 2 and original_shape[2] or 1}")

    # --- Melakukan Operasi Sesuai Pilihan ---
    result_image = None # Variabel untuk menampung hasil
    output_filename_suffix = "" # String untuk ditambahkan ke nama file output

    print(f"Info: Melakukan operasi '{args.operation}'...")
    if args.operation == 'brightness':
        result_image = adjust_brightness(image, args.value)
        output_filename_suffix = f"brightness_{args.value}"
    elif args.operation == 'contrast':
        result_image = adjust_contrast(image, args.value)
        output_filename_suffix = f"contrast_{args.value}"
    elif args.operation == 'negative':
        result_image = image_negative(image)
        output_filename_suffix = "negative"
    elif args.operation == 'threshold':
        result_image = apply_threshold(image, args.value)
        # Hasil threshold selalu grayscale
        output_filename_suffix = f"threshold_{args.value}"
    elif args.operation == 'grayscale':
        result_image = to_grayscale(image, method=args.method)
        if result_image is not None: # Jika konversi berhasil
             output_filename_suffix = f"grayscale_{args.method}"
        # Jika result_image adalah None (karena error di to_grayscale), proses penyimpanan akan dilewati


    # --- Menyimpan Hasil ---
    if result_image is not None:
        # Dapatkan nama file asli tanpa path dan tanpa ekstensi
        base_filename = os.path.splitext(os.path.basename(args.input))[0]

        # Tentukan ekstensi file output
        # Jika hasilnya Grayscale atau Threshold, gunakan PNG (lossless)
        # Jika tidak, gunakan JPG (lossy, ukuran lebih kecil)
        if len(result_image.shape) == 2 or args.operation == 'threshold':
             output_extension = ".png"
        else:
             # Pertahankan 3 channel jika hasil berwarna, misal brightness/contrast/negative dari citra warna
             output_extension = ".jpg"

        # Buat nama file output yang deskriptif
        # Format: nama_asli_operasi_nilai.ekstensi
        output_filename = f"{base_filename}_{output_filename_suffix}{output_extension}"

        # Gabungkan path folder output dengan nama file output
        output_path = os.path.join(args.output_dir, output_filename)

        print(f"Info: Menyimpan hasil ke {output_path}...")
        try:
            # Simpan citra hasil menggunakan OpenCV
            success = cv2.imwrite(output_path, result_image)
            if success:
                print(f"=== Sukses! Hasil operasi '{args.operation}' disimpan di: {output_path} ===")
            else:
                 print(f"Error: OpenCV melaporkan kegagalan saat menyimpan ke {output_path} (tanpa exception). Periksa izin folder atau path.")
        except Exception as e:
            # Tangkap jika ada error saat menyimpan (misal: path tidak valid, dll)
            print(f"Error: Terjadi kesalahan saat mencoba menyimpan hasil: {e}")
            print("Pastikan path output valid dan Anda memiliki izin menulis ke folder tersebut.")
    else:
        # Ini terjadi jika operasi gagal (misal format tidak didukung atau metode salah)
        print(f"Warning: Operasi '{args.operation}' tidak menghasilkan output atau gagal dieksekusi.")
        print("Periksa pesan error/info sebelumnya.")


# Baris ini memastikan fungsi main() hanya dijalankan
# ketika script ini dieksekusi secara langsung (bukan saat diimpor sebagai modul)
if __name__ == "__main__":
    print("--- Memulai Program Manipulasi Citra ---")
    main() # Panggil fungsi utama
    print("--- Program Selesai ---")