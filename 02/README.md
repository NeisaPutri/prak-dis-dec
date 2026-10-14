# Praktikum Pertemuan 02

## Nama : NEISA PUTRI SYIFAUL QOLBY

## Nim : 255410020

## Kelas : Informatika-1
---

## Bagian 1: Pengelolaan Proses pada Sistem Operasi

### 1. Memeriksa Sistem Operasi dan PowerShell
Memeriksa versi PowerShell dan sistem operasi yang digunakan.
![PowerShell dan Sistem Operasi](images/01-powershell-dan-sistem-operasi.png)

### 2. Menampilkan Proses yang Berjalan
- **Menggunakan Task Manager**:
  ![Daftar Proses Task Manager](images/02-daftar-proses-task-manager.png)

- **Menggunakan PowerShell**:
  Perintah: `Get-Process | Select-Object Id, ProcessName, CPU`
  ![Daftar Proses PowerShell](images/03-daftar-proses-powershell.png)

### 3. Menjalankan Aplikasi dan Menemukan PID
Membuka aplikasi untuk mendapatkan identifikasi Process ID (PID).
- **Aplikasi Dijalankan**:
  ![Aplikasi Dijalankan](images/04-chrome-dijalankan.png)

- **Memeriksa PID Aplikasi**:
  Perintah: `Get-Process <nama_aplikasi>`
  ![PID Aplikasi](images/05-pid-chrome.png)

### 4. Menghentikan Proses Menggunakan Command Line
Menghentikan aplikasi langsung dari PowerShell menggunakan PID tanpa menggunakan tombol 'X' pada aplikasi.
- **Stop Process Normal**:
  Perintah: `Stop-Process -Id <PID>`
  ![Stop Proses dengan PID](images/06-stop-proses-dengan-pid.png)

- **Menjalankan Ulang dan Cek PID Baru**:
  Saat aplikasi dijalankan kembali, sistem operasi memberikan PID baru yang berbeda.
  ![Aplikasi dan PID Baru](images/07-aplikasi-dan-pid-baru.png)

- **Penghentian Paksa (Force Kill)**:
  Perintah: `Stop-Process -Id <PID> -Force`
  ![Force Kill Proses](images/08-force-kill-proses.png)

---

## Bagian 2: Implementasi GraphQL Server dan Client

### 1. Persiapan Workspace dan Environment
- **Membuat Workspace `workspace-01`**:
  ![Workspace 01 Windows](images/09-workspace-01-windows.png)

- **Memeriksa Versi `uv`**:
  ![UV Version](images/10-uv-version-windows.png)

- **Instalasi Python 3.14**:
  ![Python 3.14 Installed](images/11-python-314-installed-windows.png)

- **Aktivasi Virtual Environment**:
  ![Virtual Environment Aktif](images/12-virtual-environment-aktif-windows.png)

- **Instalasi Paket Strawberry GraphQL & Uvicorn**:
  ![Instalasi Strawberry](images/13-instalasi-strawberry-windows.png)

---

### 2. Kode GraphQL Server (`workspace-01/schema.py`)
File `schema.py` berfungsi untuk membangun server GraphQL yang menyediakan data daftar buku.

```python
import strawberry
from strawberry.asgi import GraphQL

@strawberry.type
class Book:
    title: str
    author: str

@strawberry.type
class Query:
    @strawberry.field
    def books(self) -> list[Book]:
        return [
            Book(
                title="Distributed Systems",
                author="Andrew S. Tanenbaum",
            ),
            Book(
                title="The Pragmatic Programmer",
                author="David Thomas",
            ),
        ]

schema = strawberry.Schema(query=Query)
app = GraphQL(schema)
 
```
## Pengujian Server GraphQL

1. Menjalankan server Strawberry dengan Uvicorn:

![Server Running](./images/14-server-running.png)

2. Pengujian Query `books` di GraphQL Playground Browser:

![GraphQL Playground](./images/15-graphql-playground.png)
































<p align="center">

**Praktikum Pert 2 — Git dan GitHub**

*Sistem Terdistribusi dan Terdesentralisasi*

</p>