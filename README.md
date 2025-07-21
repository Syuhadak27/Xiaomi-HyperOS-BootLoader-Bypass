
---

# 🔓 Xiaomi Unlock Automation Script (Redmi Note 14 5G / Beryl)

Script Python ini digunakan untuk **mengirim permintaan unlock (bootloader unlock)** secara otomatis ke server Xiaomi (`https://sgp-api.buy.mi.com`) tepat di awal hari waktu Beijing (UTC+8).  
Script ini bekerja dengan **sinkronisasi NTP**, **pengukuran delay jaringan**, dan **pengiriman request yang presisi** agar peluang unlock meningkat.

---

## 📱 Kompatibilitas
✅ Telah diuji dan **berhasil** di perangkat:
- **Redmi Note 14 5G** (codename: `beryl`)
- Menggunakan Termux Android
- Koneksi internet stabil

---

## 📦 Fitur Utama

- ✅ Otomatis ambil waktu Beijing dari NTP server
- ✅ Hitung delay jaringan (ping) ke server Xiaomi
- ✅ Kirim request unlock **tepat pukul 00:00 waktu Beijing**
- ✅ Deteksi status akun (eligible / ditolak / menunggu)

---

## ⚙️ Cara Install di Termux (Langkah demi langkah)

### 1. 📥 Install Termux dan Update
```bash
pkg update && pkg upgrade
pkg install python git openssl libffi clang make

2. 🔃 Clone Repositori

git clone https://github.com/username/unlock-xiaomi-auto.git
cd unlock-xiaomi-auto

3. 📦 Install Dependencies

pip install --upgrade pip
pip install -r requirements.txt

Jika ada error SSL (ssl module is not available), lakukan reinstall Python:

pkg uninstall python
pkg install python

Kemudian ulangi perintah pip install di atas.


---

🔐 Cara Mendapatkan new_bbs_serviceToken

1. Gunakan Firefox Beta di Android


2. Buka situs: https://buy.mi.com/global


3. Login akun Xiaomi kamu


4. Install Add-on "Cookie Editor"

Link Extension (Add-on)



5. Setelah login sukses, buka Cookie Editor


6. Cari cookie dengan nama: new_bbs_serviceToken


7. Salin nilainya




---

🕒 Waktu Menjalankan Script

> Jalankan script ini sekitar pukul 22:57 – 22:59 WIB



Kenapa?

Script akan menghitung ping pada pukul 23:59:30 waktu Beijing (22:59:30 WIB)

Lalu mengirim request unlock tepat pukul 00:00:00 waktu Beijing



---

🚀 Menjalankan Script

1. Ubah config.py (opsional)

# config.py

COOKIE_VALUE = "ISI_TOKEN_MU_DI_SINI"
DEVICE_ID = ""  # Biarkan kosong untuk generate otomatis

2. Jalankan Script

python main.py

Script akan otomatis:

Mengecek status akun

Menyinkronkan waktu dengan server

Menghitung delay jaringan

Menunggu waktu ideal

Mengirim request unlock

Menampilkan hasil di terminal



---

📁 Struktur File

unlock-xiaomi-auto/
├── main.py
├── config.py
├── requirements.txt
└── README.md


---

☕ Tips Tambahan

Gunakan termux-wake-lock agar Termux tidak tertidur

Bisa digabung dengan cron/Termux Widget jika ingin otomatis harian



---

📜 Lisensi

Proyek ini bersifat eksperimental dan tidak berafiliasi dengan Xiaomi. Gunakan dengan risiko sendiri.


---

---


