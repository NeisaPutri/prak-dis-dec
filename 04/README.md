# Praktikum Pertemuan 04

## Nama : NEISA PUTRI SYIFAUL QOLBY

## Nim : 255410020

## Kelas : Informatika-1

---


# Modul 04: Konsistensi dan Replikasi pada Sistem Terdistribusi

Repositori ini berisi file konfigurasi, skrip SQL, serta laporan pengerjaan praktikum **Modul 04** untuk mata kuliah **Sistem Terdistribusi dan Terdesentralisasi**.

Praktikum ini membahas tentang penerapan basis data terdistribusi menggunakan PostgreSQL Streaming Replication dan Apache Ignite Cluster.

## Struktur Folder
- `images/`: Berisi gambar/screenshot hasil praktikum.
- `streaming-replication/`: Konfigurasi Docker dan skrip inisialisasi PostgreSQL.
- `ignite3-cluster/`: Konfigurasi Docker, `env.sh`, dan skrip SQL untuk Apache Ignite.

---

## 4.1 Streaming Replication Menggunakan PostgreSQL

Materi ini membahas konfigurasi *streaming replication* pada PostgreSQL 18 (Master-Slave) menggunakan Docker Compose[cite: 6].

### 4.1.1 Prasyarat
- Docker & Docker Compose sudah terinstal dan aktif (`dockerd`)[cite: 6].

### 4.1.2 Struktur Direktori dan File
File yang digunakan terletak pada folder `streaming-replication/`[cite: 6]:
- `00_init.sql`: Skrip pembuat user `replicator` dan slot replikasi[cite: 7].
- `docker-compose.yaml`: Konfigurasi container `postgres_primary` dan `postgres_replica`[cite: 7].
- `env.sh`: File alias perintah shell[cite: 7].

### 4.1.3 Menjalankan Docker Compose
- Menjalankan container dengan `dcu` (`source env.sh` terlebih dahulu)[cite: 9].
- Memeriksa status container (`dps`) pastikan berstatus `healthy`[cite: 9].

### 4.1.4 Pengujian Replikasi
- **Pengecekan Status Replikasi**: Mengecek `pg_stat_replication` dan `pg_replication_slots` pada primary server[cite: 11, 12], serta `pg_is_in_recovery()` pada replica server[cite: 13].
- **Manipulasi Data**:
  1. Membuat tabel `testrep` dan mengisi data pada server primary (`dep`)[cite: 14].
  2. Memeriksa sinkronisasi data pada server replica (`der`)[cite: 15].

### 4.1.5 High-Availability (HA)
- Menghentikan server primary (`docker-compose stop postgres_primary`)[cite: 16].
- Mempromosikan server replica menjadi primary menggunakan perintah `SELECT pg_promote();`[cite: 16].
- Menghentikan seluruh container (`dcd`)[cite: 17].

---

## 4.2 Replikasi Master-Master Menggunakan Apache Ignite

Materi ini membahas konfigurasi *cluster* dan replikasi multi-master pada Apache Ignite 3.1.0[cite: 17].

### 4.2.1 Prasyarat & 4.2.2 Struktur Direktori
File yang digunakan terletak pada folder `ignite3-cluster/`:
- `docker-compose.yaml`: Konfigurasi 3 node Apache Ignite (`node1`, `node2`, `node3`)[cite: 18].
- `env.sh`: File alias untuk mempermudah eksekusi CLI[cite: 18].
- `sql/`: Folder berisi dataset dan skrip query SQL (`schema.sql`, `tracks.sql`, dll)[cite: 18, 21].

### 4.2.3 Menjalankan Docker Compose
- Mengaktifkan cluster 3 node (`dcu`)[cite: 18].
- Memeriksa port (10300-10302) dan IP address masing-masing node (`docker inspect`)[cite: 18, 19].

### 4.2.4 Inisialisasi Cluster
- Menjalankan Apache Ignite CLI (`dcli`)[cite: 18, 20].
- Inisialisasi cluster: `cluster init --name ignite3 --metastorage-group=node1,node2,node3`[cite: 20].

### 4.2.5 Eksekusi Perintah SQL & Pengujian Master-Master
- Menjalankan skrip SQL dari `node1` (port 10300)[cite: 21, 22, 24].
- Verifikasi propagasi data ke `node2` (port 10301) dan `node3` (port 10302)[cite: 24, 25, 27].
- Menjalankan sampel kueri analitik *Monthly Sales Summary*[cite: 25, 26, 27].
- Menghentikan cluster (`dcd`)[cite: 27].

---

## 📸 Dokumentasi & Screenshot
*Seluruh screenshot bukti eksekusi langkah-langkah di atas disimpan dalam direktori `images/`.*