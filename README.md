# Proyek Manipulasi Citra - Operasi Titik (Intensitas)

Proyek ini adalah program Python sederhana yang menggunakan OpenCV dan NumPy untuk melakukan beberapa operasi titik dasar pada citra digital, seperti penyesuaian kecerahan, kontras, negasi, thresholding, dan konversi ke grayscale.

## Struktur Folder

Pastikan struktur folder Anda seperti berikut:

Manipulasi_Warna_WajahSendiri/
├── venv/
├── data/
│   ├── input/
│   │   └── nama_gambar_anda.jpg
│   └── output/
├── src/
│   ├── init.py
│   ├── point_operations.py
│   └── main.py
├── requirements.txt
└── README.md

## Setup (Pengaturan Awal)

1.  **Clone/Download Proyek:** Dapatkan semua file ini.
2.  **Buat Virtual Environment:**
    * Buka terminal/command prompt di folder `Manipulasi_Warna_WajahSendiri`.
    * Jalankan: `python -m venv venv`
3.  **Aktifkan Virtual Environment:**
    * Windows: `venv\Scripts\activate`
    * macOS/Linux: `source venv/bin/activate`
4.  **Install Dependencies:**
    * Pastikan venv aktif, lalu jalankan: `pip install -r requirements.txt`
5.  **Siapkan Gambar Input:** Letakkan file gambar yang ingin Anda proses di dalam folder `data/input/`.

## Cara Menjalankan Program

Semua operasi dijalankan melalui script `src/main.py` dari terminal. Pastikan Anda berada di direktori utama proyek (`Manipulasi_Warna_WajahSendiri/`) dan virtual environment Anda aktif.

**Format Perintah Umum:**

```bash
python src/main.py -i <path_ke_gambar_input> -o <path_ke_folder_output> -op <nama_operasi> [opsi_tambahan]

Argumen:

-i atau --input: Wajib. Path lengkap ke gambar input (contoh: data/input/ari_satoru.jpg).
-o atau --output_dir: Wajib. Path ke folder tempat menyimpan hasil (contoh: data/output).
-op atau --operation: Wajib. Jenis operasi yang ingin dilakukan. Pilihan: brightness, contrast, negative, threshold, grayscale.
-v atau --value: Wajib untuk brightness, contrast, threshold. Nilai integer untuk operasi tersebut.
-m atau --method: Opsional, hanya untuk grayscale. Pilihan: opencv (default) atau numpy.
Contoh Perintah Lengkap ada di bagian "Cara Memanggil yang Mudah Dimengerti" di bawah.

**Cara Menjalankan Program (Cara Memanggil yang Mudah Dimengerti)**

1.  **Buka Terminal atau Command Prompt.**
2.  **Aktifkan Virtual Environment:**
    * Pindah direktori ke folder proyek Anda: `cd path\ke\Manipulasi_Warna_WajahSendiri`
    * Jalankan: `venv\Scripts\activate` (Windows) atau `source venv/bin/activate` (Mac/Linux). Anda akan melihat `(venv)` di awal prompt.
3.  **Jalankan Perintah:** Gunakan format `python src/main.py ...` diikuti argumen yang sesuai. Ganti `data/input/ari_satoru.jpg` dengan path gambar Anda jika berbeda.

**Contoh-contoh Perintah (Copy-Paste):**

* **Mencerahkan Gambar (Brightness +50):**
    ```bash
    python src/main.py -i data/input/ari_satoru.jpg -o data/output -op brightness -v 50
    ```

* **Menggelapkan Gambar (Brightness -30):**
    ```bash
    python src/main.py -i data/input/ari_satoru.jpg -o data/output -op brightness -v -30
    ```

* **Menambah Kontras (+40):**
    ```bash
    python src/main.py -i data/input/ari_satoru.jpg -o data/output -op contrast -v 40
    ```

* **Mengurangi Kontras (-25):**
    ```bash
    python src/main.py -i data/input/ari_satoru.jpg -o data/output -op contrast -v -25
    ```

* **Membuat Negatif:**
    ```bash
    python src/main.py -i data/input/ari_satoru.jpg -o data/output -op negative
    ```

* **Membuat Thresholding (Ambang 128):**
    ```bash
    python src/main.py -i data/input/ari_satoru.jpg -o data/output -op threshold -v 128
    ```

* **Mengubah ke Grayscale (Metode OpenCV - Default):**
    ```bash
    python src/main.py -i data/input/ari_satoru.jpg -o data/output -op grayscale
    ```
    *atau bisa juga eksplisit:*
    ```bash
    python src/main.py -i data/input/ari_satoru.jpg -o data/output -op grayscale -m opencv
    ```

* **Mengubah ke Grayscale (Metode NumPy - Rata-rata):**
    ```bash
    python src/main.py -i data/input/ari_satoru.jpg -o data/output -op grayscale -m numpy
    ```

Setelah menjalankan setiap perintah, periksa folder `data/output`. Anda akan menemukan file gambar hasil operasi di sana dengan nama yang sesuai. Jika ada error, pesan error akan ditampilkan di terminal.

# Penjelasan src/point_operations.py:

File ini berisi semua fungsi logika untuk melakukan setiap operasi (Brightness, Contrast, Negative, Threshold, Grayscale).

Setiap fungsi dirancang untuk menerima citra (sebagai array NumPy) dan parameter yang diperlukan (seperti value atau method).

Fungsi mengembalikan citra hasil manipulasi (juga sebagai array NumPy).

Ada penanganan dasar jika citra input sudah grayscale atau formatnya tidak sesuai.

Metode konversi grayscale (OpenCV/NumPy) bisa dipilih.

# Penjelasan src/main.py:

* Import: Memuat library yang dibutuhkan (cv2, argparse, os, sys) dan fungsi-fungsi dari point_operations.py.

* argparse: Bagian ini mendefinisikan argumen-argumen (--input, --output_dir, --operation, --value, --method) yang bisa Anda berikan saat menjalankan program dari command line. Ini membuat program fleksibel.

Validasi Input: Kode memeriksa apakah file input ada, apakah folder output ada (jika tidak ada, coba dibuat), dan apakah argumen --value diberikan untuk operasi yang memerlukannya.

Memuat Citra: Menggunakan cv2.imread() untuk membaca file gambar.

Logika Utama: Berdasarkan nilai --operation yang Anda berikan, blok if/elif akan memanggil fungsi yang sesuai dari point_operations.py.

Menyimpan Hasil: Membuat nama file output yang deskriptif (misal: nama_asli_brightness_50.jpg) dan menyimpannya ke folder output menggunakan cv2.imwrite(). Ada penanganan error jika penyimpanan gagal.

if __name__ == "__main__":: Standar Python untuk menjalankan fungsi main() saat script dieksekusi.

Penjelasan .gitignore:
venv/, .venv/: Mengabaikan folder virtual environment.
__pycache__/, *.pyc: Mengabaikan file cache Python.
.vscode/, .idea/: Mengabaikan folder konfigurasi editor (sesuaikan jika Anda pakai editor lain).
data/output/: Penting! Mengabaikan folder output agar hasil gambar tidak ikut ter-upload ke Git. Biasanya kita hanya mengupload kode sumber dan data input sampel jika perlu.