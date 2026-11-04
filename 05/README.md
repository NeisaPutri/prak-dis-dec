# Praktikum Pertemuan 05

## Nama : NEISA PUTRI SYIFAUL QOLBY

## Nim : 255410020

## Kelas : Informatika-1

---

## MODUL 5: FAULT TOLERANCE

Repositori ini berisi file konfigurasi, Dockerfile, skrip Python, serta laporan pengerjaan praktikum **Modul 05** untuk mata kuliah **Sistem Terdistribusi dan Terdesentralisasi**.

---

## Struktur Folder
- `images/`: Berisi seluruh gambar/screenshot hasil praktikum dari setiap langkah.
- `blacksheep_lb/`: Konfigurasi server aplikasi BlackSheep dan skrip `dev.py`.
- `nginx/`: Konfigurasi Nginx sebagai Load Balancer.
- `heartbeat/`: Skrip penguji server (`check-server.py`).
- `failure-detection/`: Skrip `check-retry.py` dan `check-circuit-breaker.py`.
- `docker-compose.yml`: File orkestrasi Docker Compose.

---

## 4.1 Load Balancing Aplikasi

### 1. Persiapan
Pada tahap awal, dilakukan penyiapan *environment* menggunakan manajer `uv` serta instalasi pustaka utama `blacksheep` dan `blacksheep-cli`.

Perintah yang dijalankan di terminal:
```powershell
uv venv
.venv\Scripts\activate
uv pip install blacksheep
uv pip install blacksheep-cli

---
```

### 2. Pembuatan Aplikasi Web
Aplikasi web berbasis ASGI dibuat menggunakan perintah `blacksheep create` dengan nama proyek `blacksheep_lb`, kemudian pustaka dependensi diinstal melalui `requirements.txt`.

Perintah yang dijalankan:
```powershell
blacksheep create
cd blacksheep_lb
uv pip install -r requirements.txt
py dev.py

```
---

### 3. Siapkan Dockerfile dan docker-compose.yml
Menyiapkan konfigurasi struktur direktori, Dockerfile untuk aplikasi dan Nginx, serta file `docker-compose.yml` untuk orkestrasi service.

Perintah untuk memeriksa struktur direktori:
```powershell
ls -la
```

---

### 4. Menjalankan Docker Compose
Menjalankan perintah orkestrasi Docker Compose untuk membangun image dan mengaktifkan instance aplikasi serta Nginx secara bersamaan.

Perintah yang dijalankan:
```powershell
docker-compose up --build -d --scale bs_app=2
```
---

## 4.2 Failure Detection

### 5. Pengujian Heartbeat
Protokol heartbeat digunakan untuk memantau aktivitas suatu komponen server. Pengujian dilakukan menggunakan skrip check-server.py pada kondisi server aktif maupun non-aktif.   
Perintah yang dijalankan:

```powerShell
python check-server.py localhost 44777
python check-server.py localhost 80
```
---

### 6. Pengujian Retry dengan Tenacity
Pustaka tenacity digunakan untuk mengelola proses koneksi berulang (retry) guna mengantisipasi kegagalan komunikasi antar komponen.

Perintah yang dijalankan:

```powerShell
python check-retry.py
```
---

### 7. Pengujian Circuit Breaker
Pola circuit breaker berfungsi untuk mencegah kegagalan berantai dengan memblokir sementara panggilan ke layanan yang gagal.   

Perintah yang dijalankan:

```powerShell
python check-circuit-breaker.py
```
---