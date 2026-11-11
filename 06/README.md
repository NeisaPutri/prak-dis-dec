# Praktikum Pertemuan 06

## Nama : NEISA PUTRI SYIFAUL QOLBY

## Nim : 255410020

## Kelas : Informatika-1

---

# A. TUJUAN

Praktikum ini bertujuan untuk:
1. Memahami konsep *Distributed File System* dan fungsi HDFS pada Apache Hadoop.
2. Menyiapkan Java Development Kit (JDK) dan Apache Hadoop sebagai prasyarat penggunaan HDFS.
3. Mengatur variabel lingkungan Hadoop, terutama `JAVA_HOME`.
4. Mengonfigurasi alamat *default filesystem* dan jumlah replikasi blok HDFS.
5. Menyiapkan konfigurasi dasar Hadoop dan HDFS sebelum layanan dijalankan.

---

# B. DASAR TEORI

## 1. Apache Hadoop dan HDFS

Apache Hadoop adalah perangkat lunak untuk menyimpan dan memproses data pada lingkungan terdistribusi. Hadoop Distributed File System (HDFS) merupakan sistem berkas Hadoop yang membagi berkas menjadi blok-blok dan menyimpannya pada node yang dikelola dalam sebuah klaster. Dengan cara ini, data berukuran besar dapat dikelola pada lebih dari satu komputer.

## 2. Komponen HDFS

NameNode mengelola metadata sistem berkas, seperti struktur direktori dan lokasi blok. DataNode menyimpan blok data yang sebenarnya dan melayani operasi baca maupun tulis. Klien HDFS berinteraksi dengan NameNode untuk memperoleh informasi berkas, kemudian mengakses data pada DataNode.

## 3. Replikasi Data

HDFS dapat menyimpan salinan blok pada beberapa DataNode agar data tetap tersedia ketika terjadi gangguan. Banyaknya salinan diatur melalui properti `dfs.replication` pada `hdfs-site.xml`. Untuk konfigurasi satu node seperti yang ditunjukkan pada bukti praktikum, nilai `1` digunakan agar jumlah salinan sesuai dengan lingkungan lokal.

## 4. Konfigurasi Dasar Hadoop

Properti `fs.defaultFS` pada `core-site.xml` menentukan alamat filesystem yang digunakan klien, sedangkan variabel `JAVA_HOME` memberi tahu Hadoop lokasi instalasi Java. JDK 17 digunakan sebagai versi Java server pada petunjuk modul. Lokasi `JAVA_HOME` harus disesuaikan dengan direktori JDK pada komputer yang digunakan.

---

# C. PEMBAHASAN

## 1. Unduh Apache Hadoop

Modul mengarahkan praktikan untuk mengambil distribusi Apache Hadoop dari halaman rilis resmi dan menggunakan versi `3.5.0`.

<img src="images/01-jdk-install.png" width="700">

**Penjelasan:**
Screenshot yang tersedia memperlihatkan halaman unduh resmi Apache Hadoop. Walaupun nama file memuat kata `jdk`, isi gambar adalah halaman unduh Hadoop; karena itu gambar ini diletakkan pada langkah pengunduhan Apache Hadoop.

---

## 2. Instalasi Apache Hadoop

Modul mencontohkan ekstraksi arsip Hadoop ke direktori penyimpanan, pembuatan tautan `hadoop`, lalu konfigurasi lingkungan agar perintah Hadoop dapat digunakan:

```bash
cd ~/software/storage/
tar -xvf ~/master/data-engineering/apache-hadoop/hadoop-3.5.0.tar.gz
ln -s hadoop-3.5.0 hadoop
```

Direktori instalasi tersebut selanjutnya disebut `$HADOOP_HOME`. Setiap kali membuka shell baru, muat konfigurasi Hadoop dan jalankan perintah `hadoop` untuk memeriksa instalasi:

```bash
source ~/env/bash/storage/hadoop.sh
hadoop
```

<img src="images/02-hadoop-extract.png" width="700">

<img src="images/02-hadoop-path-check.png" width="700">

**Penjelasan:**
Screenshot pertama tersedia dan menunjukkan isi direktori hasil ekstraksi Hadoop, termasuk folder `bin`, `etc`, `lib`, dan `sbin`. Tambahkan screenshot kedua untuk bukti konfigurasi lingkungan atau keluaran perintah `hadoop`; file gambar tersebut belum tersedia.

---

## 3. Instalasi pdsh

Modul menjelaskan bahwa cara pemasangan `pdsh` menyesuaikan distribusi Linux. Pada Artix Linux, `pdsh` dipasang dari AUR menggunakan `trizen`. Setelah terpasang, periksa bahwa program dapat dijalankan. Jika tipe `Rcmd` yang digunakan bukan SSH, atur variabel lingkungan berikut:

```bash
export PDSH_RCMD_TYPE=ssh
```

<img src="images/03-pdsh-install.png" width="700">

<img src="images/04-pdsh-verify.png" width="700">

**Penjelasan:**
Tambahkan screenshot pemasangan `pdsh` dan screenshot pemeriksaan program atau konfigurasi `PDSH_RCMD_TYPE`. Kedua bukti ini belum tersedia di folder `images`.

### Menyiapkan SSH agar koneksi ke localhost tidak memerlukan login

Modul meminta praktikan menyiapkan kunci SSH agar koneksi ke `localhost` dapat dilakukan tanpa memasukkan kata sandi:

```bash
ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 0600 ~/.ssh/authorized_keys
```

<img src="images/05-ssh-key-setup.png" width="700">

<img src="images/06-ssh-localhost-test.png" width="700">

**Penjelasan:**
Tambahkan screenshot pembuatan kunci dan pengaturan `authorized_keys`, kemudian screenshot pengujian koneksi SSH ke `localhost`. Bukti-bukti tersebut belum tersedia di folder `images`. Pastikan layanan `sshd` sudah berjalan, sesuai persyaratan modul.

---

## 4. Konfigurasi Apache Hadoop

Modul meminta konfigurasi berikut pada direktori `$HADOOP_HOME/etc/hadoop/`.

### `hdfs-site.xml`

```xml
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
</configuration>
```

<img src="images/07-hdfs-site..png" width="700">

**Penjelasan:**
Screenshot tersedia dan menunjukkan `dfs.replication` diatur ke `1`.

### `core-site.xml`

```xml
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://localhost:9000</value>
    </property>
    <property>
        <name>hadoop.proxyuser.yourusername.groups</name>
        <value>*</value>
    </property>
    <property>
        <name>hadoop.proxyuser.yourusername.hosts</name>
        <value>*</value>
    </property>
</configuration>
```

Ganti `yourusername` dengan nama pengguna yang sesuai.

<img src="images/08-xml-configs.png" width="700">

<img src="images/09-core-site-proxyuser.png" width="700">

**Penjelasan:**
Screenshot pertama tersedia dan menunjukkan `fs.defaultFS` bernilai `hdfs://localhost:9000`. Tambahkan screenshot kedua apabila bukti konfigurasi properti `hadoop.proxyuser...` belum tercakup dalam gambar pertama.

### `mapred-site.xml`

```xml
<configuration>
    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>
    <property>
        <name>mapreduce.application.classpath</name>
        <value>$HADOOP_CLASSPATH:$HADOOP_HOME/share/hadoop/mapreduce/*:$HADOOP_MAPRED_HOME/share/hadoop/mapreduce/lib/*</value>
    </property>
</configuration>
```

<img src="images/10-mapred-site.png" width="700">

**Penjelasan:**
Tambahkan screenshot konfigurasi `mapred-site.xml`; file gambar tersebut belum tersedia.

### `yarn-site.xml`

```xml
<configuration>
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
    <property>
        <name>yarn.nodemanager.env-whitelist</name>
        <value>JAVA_HOME,HADOOP_COMMON_HOME,HADOOP_HDFS_HOME,HADOOP_CONF_DIR,CLASSPATH_PREPEND_DISTCACHE,HADOOP_YARN_HOME,HADOOP_HOME,PATH,LANG,TZ,HADOOP_MAPRED_HOME</value>
    </property>
    <property>
        <name>yarn.nodemanager.resource.memory-mb</name>
        <value>4096</value>
    </property>
    <property>
        <name>yarn.scheduler.minimum-allocation-mb</name>
        <value>2048</value>
    </property>
    <property>
        <name>yarn.nodemanager.vmem-pmem-ratio</name>
        <value>2.1</value>
    </property>
</configuration>
```

<img src="images/11-yarn-site.png" width="700">

**Penjelasan:**
Tambahkan screenshot konfigurasi `yarn-site.xml`; file gambar tersebut belum tersedia.

---

## 5. Format NameNode

Modul mengingatkan bahwa proses ini cukup dilakukan satu kali. Jika dilakukan kembali, berkas yang sudah diproses di HDFS dapat terhapus. Jalankan format NameNode satu kali:

```bash
hdfs namenode -format
```

<img src="images/07-namenode-format.png" width="700">

**Penjelasan:**
Tambahkan screenshot hasil perintah format NameNode. Bukti ini belum tersedia di folder `images`.

---

## 6. Atur konfigurasi JAVA_HOME

Modul meminta praktikan mengedit `$HADOOP_HOME/etc/hadoop/hadoop-env.sh` dan mengisi `JAVA_HOME` sesuai lokasi JDK pada komputer, server, atau node.

<img src="images/13-hadoop-env-config.png" width="700">

**Penjelasan:**
Kedua screenshot tersedia dan memperlihatkan konfigurasi `JAVA_HOME` pada `hadoop-env.cmd` di Windows.

---

## 7. Jalankan daemon untuk HDFS

Setelah konfigurasi Hadoop selesai, jalankan daemon HDFS sesuai lingkungan instalasi. Untuk shell Linux pada distribusi Hadoop, gunakan skrip:

```bash
start-dfs.sh
```

Modul menyebutkan bahwa pemantauan layanan dapat dilakukan melalui web setelah daemon berjalan.

<img src="images/14-hdfs-daemon-start.png" width="700">

<img src="images/15-hdfs-web-monitor.png" width="700">

**Penjelasan:**
Tambahkan screenshot pertama untuk bukti menjalankan daemon HDFS dan screenshot kedua untuk bukti pemantauan melalui web. Kedua gambar belum tersedia di folder `images`.

---

**Batas pembahasan:** Susunan pembahasan ini mengikuti judul langkah utama pada modul dari pengunduhan Apache Hadoop sampai menjalankan daemon HDFS. Persyaratan software merupakan prasyarat (langkah 0) dan tidak dijadikan langkah pembahasan. Pengaturan SSH ditempatkan sebagai bagian dari instalasi `pdsh`, sesuai susunan modul. Operasi berkas, penghentian HDFS, dan tugas CSV yang dijelaskan setelahnya tidak termasuk dalam pembahasan ini.

---

# D. KESIMPULAN

Berdasarkan Modul 06, langkah utama praktikum dimulai dari mengunduh dan menginstal Apache Hadoop, dilanjutkan dengan instalasi `pdsh`, konfigurasi Hadoop, format NameNode, pengaturan `JAVA_HOME`, dan menjalankan daemon HDFS. Persiapan SSH disertakan dalam bagian instalasi `pdsh`. Screenshot yang tersedia ditempatkan pada langkah yang sesuai, sedangkan pemanggilan gambar yang belum tersedia disiapkan untuk dilengkapi.


<p align="center">

**Praktikum Pertemuan 06 — Distributed File System (HDFS)**

*Sistem Terdistribusi dan Terdesentralisasi*

</p>