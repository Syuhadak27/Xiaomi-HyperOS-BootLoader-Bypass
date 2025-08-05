

---

## 🔓 Xiaomi Unlock Automation Scrip


(Redmi Note 14 5G / Beryl)

Script Python ini digunakan untuk mengirim permintaan unlock bootloader secara otomatis ke server Xiaomi (https://sgp-api.buy.mi.com) tepat di awal hari waktu Beijing (UTC+8).

Script bekerja dengan:

Sinkronisasi waktu via NTP

Pengukuran delay jaringan

Pengiriman request yang sangat presisi


...untuk meningkatkan peluang unlock yang berhasil.


---

📱 Kompatibilitas

✅ Telah diuji dan berhasil di:

Redmi Note 14 5G (codename: beryl)

Lingkungan Termux (Android)

Koneksi internet stabil



---

📦 Fitur Utama

✅ Sinkronisasi waktu Beijing via NTP

✅ Penghitungan delay (ping) ke server Xiaomi

✅ Pengiriman request tepat pukul 00:00:00 waktu Beijing

✅ Deteksi status akun: eligible / ditolak / menunggu



---

⚙️ Cara Instalasi di Termux (Step-by-step)

1. 📥 Update Termux

```bash
pkg update && pkg upgrade
```

2. 📦 Install Dependensi Utama

```bash
pkg install python git openssl libffi clang make
```

3. 🔃 Clone Repositori
```bash
git clone https://github.com/Syuhadak27/Xiaomi-HyperOS-BootLoader-Bypass.git bypass
cd bypass
```

4. 📦 Install Modul Python

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

> Jika muncul error seperti ssl module is not available, lakukan reinstall Python:



```bash
pkg uninstall python
pkg install python
```


> Lalu ulangi instalasi dependensi di atas.




---

🔐 Cara Mendapatkan new_bbs_serviceToken

1. Gunakan Firefox Beta (Android)


2. Buka situs: https://buy.mi.com/global


3. Login menggunakan akun Xiaomi kamu


4. Install ekstensi Cookie Editor


5. Setelah login sukses, buka Cookie Editor


6. Cari cookie bernama: new_bbs_serviceToken


7. Salin nilainya




---

🕒 Waktu Menjalankan Script

> Jalankan sekitar pukul 22:57 – 22:59 WIB



Mengapa?
Script akan mulai menghitung ping pada:

23:59:30 waktu Beijing (setara 22:59:30 WIB)

Kemudian mengirim request tepat pada:

00:00:00 waktu Beijing (23:00:00 WIB)


---

🚀 Menjalankan Script

1. Edit config.py dan masukkan token milikmu

# config.py

```bash
COOKIE_VALUE = "ISI_TOKEN_MU_DI_SINI"
DEVICE_ID = ""  # Biarkan kosong untuk generate otomatis
```

2. Jalankan Script

```bash
python main.py
```

Script akan otomatis melakukan:

Mengecek status akun

Menyinkronkan waktu dengan server

Mengukur delay jaringan

Menunggu waktu ideal

Mengirim request unlock

Menampilkan hasil di terminal


> Setelah selesai, jangan tutup terminal.
Logout akun Mi di pengaturan, login kembali, masuk ke Developer Options, dan tambahkan perangkat.




---

📜 Lisensi

Proyek ini bersifat eksperimental dan tidak berafiliasi dengan Xiaomi.
Gunakan dengan risiko Anda sendiri.


---
