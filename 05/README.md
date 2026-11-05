# Praktikum Pertemuan 05

## Nama : NEISA PUTRI SYIFAUL QOLBY

## Nim : 255410020

## Kelas : Informatika-1

---

# MODUL 5: FAULT TOLERANCE

Praktikum ini membahas penerapan toleransi kesalahan pada sistem terdistribusi melalui *load balancing* dan *failure detection*. Aplikasi web BlackSheep dijalankan dalam beberapa container dan diakses melalui Nginx, kemudian ketersediaan layanan dan strategi pemulihan kegagalan dipelajari menggunakan heartbeat, retry, dan circuit breaker.

## Struktur Folder

- `images/`: Tangkapan layar langkah dan hasil praktikum.
- `load-balancing/blacksheep_lb/`: Aplikasi web BlackSheep dan Dockerfile aplikasi.
- `load-balancing/nginx/`: Dockerfile serta konfigurasi Nginx sebagai *load balancer*.
- `load-balancing/docker-compose.yml`: Orkestrasi container aplikasi dan Nginx.
- `heartbeat/check-server.py`: Skrip untuk menguji koneksi ke host dan port.
- `failure-detection/check-retry.py`: Contoh permintaan HTTP dengan mekanisme retry dari Tenacity.
- `failure-detection/check-circuit-breaker.py`: Contoh permintaan HTTP dengan mekanisme circuit breaker dari PyBreaker.

---

# A. TUJUAN

Praktikum ini bertujuan untuk:

1. Memahami konsep *fault tolerance* dan perannya dalam menjaga ketersediaan layanan pada sistem terdistribusi.
2. Menerapkan *load balancing* dengan Nginx untuk meneruskan permintaan ke beberapa instance aplikasi.
3. Menjalankan dan mengelola beberapa service menggunakan Docker Compose.
4. Memeriksa ketersediaan server menggunakan koneksi ke host dan port melalui skrip heartbeat.
5. Memahami mekanisme retry dengan jeda bertahap untuk menghadapi kegagalan koneksi sementara.
6. Memahami circuit breaker sebagai mekanisme untuk membatasi permintaan ke layanan yang terus mengalami kegagalan.

---

# B. DASAR TEORI

## 1. Fault Tolerance

*Fault tolerance* adalah kemampuan sistem untuk tetap menyediakan layanan ketika sebagian komponen mengalami kegagalan. Pada sistem terdistribusi, kegagalan jaringan, server, atau proses dapat mengganggu layanan. Redundansi dan deteksi kegagalan merupakan beberapa pendekatan untuk mengurangi dampaknya.

## 2. Load Balancing

*Load balancing* membagi atau meneruskan permintaan klien ke beberapa instance layanan. Nginx bertindak sebagai titik akses (proxy) di depan aplikasi, sedangkan Docker Compose menjalankan service aplikasi dan Nginx. Dengan lebih dari satu instance aplikasi, layanan tidak hanya bergantung pada satu container.

## 3. Failure Detection dan Heartbeat

*Failure detection* adalah proses mengidentifikasi apakah suatu layanan dapat dijangkau. Pada praktikum ini, skrip heartbeat mencoba membuka koneksi TCP ke host dan port yang diberikan. Koneksi berhasil menunjukkan server dapat dijangkau pada saat pemeriksaan; kegagalan koneksi menghasilkan status server tidak aktif.

## 4. Retry dan Circuit Breaker

Retry mencoba kembali permintaan yang gagal, biasanya dengan jeda yang meningkat (*exponential backoff*) agar tidak terus-menerus membebani layanan. Circuit breaker memantau kegagalan dan dapat membuka sirkuit setelah batas kegagalan tercapai, sehingga permintaan berikutnya dihentikan sementara sebelum layanan dicoba kembali.

---

# C. PEMBAHASAN

## 4.1 Load Balancing Aplikasi

### 1. Persiapan Lingkungan dan Dependensi

Lingkungan pengembangan disiapkan menggunakan `uv`. Pustaka BlackSheep dan CLI-nya dipasang untuk membuat serta menjalankan aplikasi web Python.

Perintah yang digunakan:

```powershell
uv venv
.venv\Scripts\activate
uv pip install blacksheep blacksheep-cli
```

Hasil instalasi pustaka ditunjukkan pada tangkapan layar berikut.

<img src="images/01_Persiapan.png" width="700">

**Penjelasan:** Keluaran terminal menunjukkan paket BlackSheep, BlackSheep CLI, dan dependensi terkait berhasil dipasang pada lingkungan praktikum.

---

### 2. Membuat dan Menjalankan Aplikasi BlackSheep

Proyek aplikasi dibuat menggunakan CLI BlackSheep dengan nama `blacksheep_lb`. Setelah dependensi proyek dipasang, aplikasi dijalankan dalam mode pengembangan.

```powershell
blacksheep create
cd blacksheep_lb
uv pip install -r requirements.txt
python dev.py
```

<img src="images/02-dev-py.png" width="700">

<img src="images/02-Dev-py2.png" width="700">

**Penjelasan:** Proyek `blacksheep_lb` berhasil dibuat. Saat dijalankan secara lokal, server Uvicorn melaporkan aplikasi aktif di `http://localhost:44777`.

---

### 3. Menyiapkan Dockerfile dan Nginx

Dockerfile aplikasi digunakan untuk membangun image aplikasi BlackSheep. Konfigurasi Nginx mendefinisikan upstream `backend` yang mengarah ke service `bs_app` pada port 80, kemudian meneruskan permintaan yang diterima di port 80 ke upstream tersebut.

<img src="images/03-struktur-folder.png" width="700">

<img src="images/04-dockerfile.png" width="700">

<img src="images/05-nginx-conf.png" width="700">

**Penjelasan:** Struktur proyek memisahkan aplikasi, konfigurasi Nginx, dan berkas orkestrasi. Konfigurasi ini menempatkan Nginx sebagai pintu masuk aplikasi di dalam jaringan Docker.

---

### 4. Membangun dan Menjalankan Container

Dari direktori `05/load-balancing`, image aplikasi dan Nginx dibangun, kemudian service dijalankan dengan dua replika aplikasi:

```powershell
docker compose up --build -d --scale bs_app=2
```

<img src="images/06-docker-compose-up.png" width="700">

**Penjelasan:** Proses build selesai dan Docker menjalankan dua container `bs_app` serta satu container `nginx`. Nginx memublikasikan port 80 container ke port 80 pada host.

---

### 5. Memeriksa Hasil Load Balancing

Aplikasi diakses melalui `http://localhost`, yaitu port yang dipublikasikan oleh Nginx. Status container dan log aplikasi diperiksa untuk memastikan instance dapat menerima permintaan.

<img src="images/07-load-balancing.png" width="700">

<img src="images/08-docker-logs.png" width="700">

<img src="images/09-docker-logs-detail..png" width="700">

**Penjelasan:** Halaman aplikasi BlackSheep berhasil ditampilkan melalui `localhost`. Daftar container memperlihatkan dua instance aplikasi dalam kondisi berjalan, dan log kedua instance mencatat permintaan HTTP dengan status `200 OK`. Hasil ini menunjukkan aplikasi dapat diakses melalui Nginx dan kedua instance menerima permintaan.

---

## 4.2 Failure Detection

### 6. Pengujian Heartbeat

Skrip `check-server.py` mencoba membuat koneksi TCP ke host dan port yang diberikan. Pengujian yang terdokumentasi pada tangkapan layar menggunakan port `44777`:

```powershell
cd 05\heartbeat
py check-server.py localhost 44777
```

<img src="images/09-heartbeat.png" width="700">

**Penjelasan:** Skrip menampilkan `Server down`, yang berarti tidak ada layanan yang menerima koneksi pada `localhost:44777` saat pengujian tersebut dilakukan. Hasil ini merupakan pemeriksaan pada kondisi saat itu; port tersebut digunakan oleh server pengembangan lokal ketika aplikasi dijalankan, sedangkan aplikasi dalam Docker diakses melalui port 80.

---

### 7. Pengujian Retry dengan Tenacity

Skrip `check-retry.py` mengirim permintaan ke `http://localhost:44777`. Dekorator Tenacity mengatur maksimal lima percobaan dan jeda eksponensial dengan nilai minimum empat detik dan maksimum sepuluh detik. Dependensi yang diperlukan adalah `tenacity` dan `requests`.

```powershell
cd 05\failure-detection
uv pip install tenacity requests
py check-retry.py
```

**Penjelasan:** Jika koneksi gagal, permintaan dicoba ulang sesuai kebijakan tersebut. Jika semua percobaan tetap gagal, skrip menangkap dan menampilkan pesan kegagalan. Berkas hasil praktikum menyediakan konfigurasi dan skrip pengujian; tangkapan layar hasil eksekusi retry tidak disertakan.

---

### 8. Pengujian Circuit Breaker dengan PyBreaker

Skrip `check-circuit-breaker.py` juga mengirim permintaan ke `http://localhost:44777`. Circuit breaker dikonfigurasi dengan batas empat kegagalan (`fail_max=4`) dan waktu reset 20 detik (`reset_timeout=20`).

```powershell
cd 05\failure-detection
uv pip install pybreaker requests
py check-circuit-breaker.py
```

**Penjelasan:** Konfigurasi tersebut mengilustrasikan ambang kegagalan dan waktu tunggu sebelum circuit breaker dapat mencoba kembali. Skrip melakukan satu pemanggilan permintaan per eksekusi; karena itu, satu kali menjalankan skrip saja belum menunjukkan empat kegagalan berturut-turut atau membuktikan bahwa sirkuit telah terbuka.

---

# D. KESIMPULAN

Berdasarkan praktikum yang telah dilakukan, dapat disimpulkan bahwa:

1. Nginx dapat digunakan sebagai *reverse proxy* untuk menerima permintaan pada port 80 dan meneruskannya ke service aplikasi BlackSheep.
2. Docker Compose berhasil menjalankan dua replika aplikasi beserta container Nginx. Halaman aplikasi dapat diakses melalui `localhost`, dan log kedua replika mencatat permintaan dengan status `200 OK`.
3. Pemeriksaan heartbeat bergantung pada ketersediaan layanan di host dan port yang diuji. Pada pengujian yang terdokumentasi, `localhost:44777` menghasilkan status `Server down`.
4. Retry dengan jeda eksponensial dan circuit breaker menyediakan pendekatan berbeda untuk menangani kegagalan komunikasi: retry mengulang permintaan, sedangkan circuit breaker membatasi percobaan ketika kegagalan melewati ambang.
5. Untuk menyimpulkan bahwa mekanisme retry berhasil pulih atau circuit breaker benar-benar terbuka, diperlukan pengujian berulang dengan layanan tersedia dan tidak tersedia serta pencatatan hasil eksekusinya.

---

<p align="center">

**Praktikum Pertemuan 05 — Fault Tolerance**

*Sistem Terdistribusi dan Terdesentralisasi*

</p>