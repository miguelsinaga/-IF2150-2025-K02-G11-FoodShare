# IF2150-2025-K02-G11-FoodShare

## Ringkas
FoodShare adalah aplikasi Python (Tkinter + CustomTkinter) untuk donasi makanan dengan tiga peran: Provider, Receiver, Admin. Aplikasi kini berjalan penuh di MySQL lokal untuk seluruh fitur (akun, donasi, request, feedback, laporan).

## Prasyarat
- Python 3.12 (direkomendasikan)
- `uv` (package manager Python)
- MySQL (5.7+/8+), berjalan di `localhost:3306`

## Instalasi & Menjalankan
1. Install dependencies dengan `uv`:
   ```sh
   uv sync
   ```
2. Jalankan aplikasi:
   ```sh
   make run
   ```

## Sat-Set Quick Start
Copy–paste perintah berikut untuk menyiapkan MySQL lokal, mengisi data contoh, dan menjalankan aplikasi.

```sh
# 1) Mulai MySQL (macOS Homebrew)
brew services start mysql

# 2) Buat database & user (abaikan jika sudah ada)
mysql -u root -e "\
CREATE DATABASE IF NOT EXISTS foodshare; \
CREATE USER IF NOT EXISTS 'foodshare_user'@'localhost' IDENTIFIED BY 'janganbuangbuangmakanan'; \
GRANT ALL PRIVILEGES ON foodshare.* TO 'foodshare_user'@'localhost'; \
FLUSH PRIVILEGES;"

# 3) Impor seed data (masukkan password saat diminta)
mysql -u foodshare_user -p foodshare < db/seed.sql

# 4) Install deps & jalankan
uv sync && make run
```

Login contoh untuk uji:
- Provider: `provider@example.com` / `123456`
- Receiver: `receiver@example.com` / `123456`
- Admin: `admin@example.com` / `123456`

## Windows Quick Start (PowerShell)
```powershell
# 1) Install MySQL (disarankan MySQL Installer dari dev.mysql.com)
#    Alternatif Chocolatey: choco install mysql

# 2) Buat database & user
mysql -u root -e "CREATE DATABASE IF NOT EXISTS foodshare;"
mysql -u root -e "CREATE USER IF NOT EXISTS 'foodshare_user'@'localhost' IDENTIFIED BY 'janganbuangbuangmakanan';"
mysql -u root -e "GRANT ALL PRIVILEGES ON foodshare.* TO 'foodshare_user'@'localhost'; FLUSH PRIVILEGES;"

# 3) Impor seed
mysql -u foodshare_user -p foodshare < db\seed.sql

# 4) Jalankan app
uv sync
python app.py
```

Jika `make` belum tersedia di Windows, gunakan `python app.py`.

## Linux Quick Start (Ubuntu/Debian)
```sh
# 1) Install & start MySQL
sudo apt update
sudo apt install -y mysql-server
sudo systemctl enable --now mysql

# 2) Buat database & user
sudo mysql -e "CREATE DATABASE IF NOT EXISTS foodshare;"
sudo mysql -e "CREATE USER IF NOT EXISTS 'foodshare_user'@'localhost' IDENTIFIED BY 'janganbuangbuangmakanan';"
sudo mysql -e "GRANT ALL PRIVILEGES ON foodshare.* TO 'foodshare_user'@'localhost'; FLUSH PRIVILEGES;"

# 3) Impor seed
mysql -u foodshare_user -p foodshare < db/seed.sql

# 4) Jalankan app
uv sync && make run
```

## WSL (Windows Subsystem for Linux)
- Ikuti langkah “Linux Quick Start” di dalam distro WSL (Ubuntu/Debian).
- Pastikan MySQL WSL berjalan (gunakan `service mysql start` jika `systemctl` tidak tersedia).
- Jalankan aplikasi dari direktori proyek yang di-mount ke WSL.

## Environment Variables (opsional)
Override kredensial MySQL jika diperlukan:
- macOS/Linux (bash/zsh):
```sh
export DB_HOST=localhost
export DB_PORT=3306
export DB_USER=foodshare_user
export DB_PASS=janganbuangbuangmakanan
export DB_NAME=foodshare
```
- Windows (PowerShell):
```powershell
$env:DB_HOST = "localhost"
$env:DB_PORT = "3306"
$env:DB_USER = "foodshare_user"
$env:DB_PASS = "janganbuangbuangmakanan"
$env:DB_NAME = "foodshare"
```

## Konfigurasi MySQL Lokal
1. Mulai MySQL (macOS):
   ```sh
   brew services start mysql
   ```
2. Buat database & user (sekali saja):
   ```sql
   CREATE DATABASE foodshare;
   CREATE USER 'foodshare_user'@'localhost' IDENTIFIED BY 'janganbuangbuangmakanan';
   GRANT ALL PRIVILEGES ON foodshare.* TO 'foodshare_user'@'localhost';
   FLUSH PRIVILEGES;
   ```
3. Pilih database:
   ```sql
   USE foodshare;
   ```
4. Buat tabel (jika belum ada):
   ```sql
   CREATE TABLE IF NOT EXISTS users (
     id INT AUTO_INCREMENT PRIMARY KEY,
     nama VARCHAR(50), email VARCHAR(60), password_hash VARCHAR(256),
     noTelepon VARCHAR(15), role VARCHAR(10), status VARCHAR(10) DEFAULT 'aktif'
   );
   CREATE TABLE IF NOT EXISTS donatur (
     id_user INT PRIMARY KEY, total_donasi INT,
     status_akun VARCHAR(15) DEFAULT 'aktif',
     FOREIGN KEY (id_user) REFERENCES users(id)
   );
   CREATE TABLE IF NOT EXISTS penerima (
     id_user INT PRIMARY KEY, alamat VARCHAR(40),
     FOREIGN KEY (id_user) REFERENCES users(id)
   );
   CREATE TABLE IF NOT EXISTS admin (
     id_user INT PRIMARY KEY,
     FOREIGN KEY (id_user) REFERENCES users(id)
   );
   CREATE TABLE IF NOT EXISTS makanan (
     id_makanan INT AUTO_INCREMENT PRIMARY KEY,
     id_donatur INT, jenis_makanan VARCHAR(40), jumlah_porsi INT,
     lokasi VARCHAR(40), batas_waktu DATETIME,
     status VARCHAR(10) DEFAULT 'layak',
     FOREIGN KEY (id_donatur) REFERENCES donatur(id_user)
   );
   CREATE TABLE IF NOT EXISTS request_donasi (
     id_request INT AUTO_INCREMENT PRIMARY KEY,
     id_penerima INT, id_makanan INT,
     status VARCHAR(15) DEFAULT 'aktif', tanggal_request DATETIME,
     FOREIGN KEY (id_penerima) REFERENCES penerima(id_user),
     FOREIGN KEY (id_makanan) REFERENCES makanan(id_makanan)
   );
   CREATE TABLE IF NOT EXISTS feedback (
     id_feedback INT AUTO_INCREMENT PRIMARY KEY,
     id_donatur INT, id_penerima INT,
     rating INT, komentar VARCHAR(100), tanggal_feedback DATETIME,
     FOREIGN KEY (id_donatur) REFERENCES donatur(id_user),
     FOREIGN KEY (id_penerima) REFERENCES penerima(id_user)
   );
   CREATE TABLE IF NOT EXISTS laporan_donasi (
     id_laporan INT AUTO_INCREMENT PRIMARY KEY,
     id_request INT, tanggal_laporan DATETIME,
     jenis_laporan VARCHAR(30), deskripsi VARCHAR(100), bukti VARCHAR(50),
     estimasi_pengurangan DECIMAL(10,2),
     FOREIGN KEY (id_request) REFERENCES request_donasi(id_request)
   );
   ```

## Seed Data
1. Impor seed:
   ```sh
   mysql -u foodshare_user -p foodshare < db/seed.sql
   ```
2. Kredensial contoh:
   - Provider: `provider@example.com` / `123456`
   - Receiver: `receiver@example.com` / `123456`
   - Admin: `admin@example.com` / `123456`

## Cara Pakai Singkat
- Provider: Login → tambah stok (Food Stock) → kelola request (Food Requests).
- Receiver: Login → pilih “Available Food” → Request → setelah Completed, kirim Feedback.
- Admin: Statistik umum (sederhana).

## Troubleshooting
- MySQL belum berjalan:
  ```sh
  brew services start mysql
  ```
- Database sudah ada: gunakan `USE foodshare;` lalu `SHOW TABLES;`.
- FK error: pastikan user ada, aplikasi otomatis membuat baris di `donatur/penerima` saat diperlukan.

## Modul Utama
- Backend: `src/backend/*_data.py`, `src/backend/mySQLConnector.py`
- Controller: `src/controller/*`
- Frontend: `src/frontend/*`
- Model: `src/model/*`
