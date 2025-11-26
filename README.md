# IF2150-2025-K02-G11-FoodShare

## Penjelasan Singkat
FoodShare adalah aplikasi berbasis Python yang bertujuan untuk menghubungkan provider makanan dengan penerima (receiver) secara efisien. Aplikasi ini mendukung donasi makanan, permintaan makanan, manajemen pengguna, dan feedback antar pengguna. Terdapat tiga peran utama: Provider, Receiver, dan Admin.

## Prasyarat dan Instalasi

### Prasyarat
- Python 3.8+
- pip (Python package manager)

### Instalasi
1. Clone repository ini:
   ```sh
   git clone https://github.com/yourusername/foodshare.git
   cd foodshare
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Jalankan aplikasi:
   ```sh
   python app.py
   ```


## Fitur
- Donasi makanan
- Permintaan makanan
- Manajemen pengguna
- Feedback antar pengguna

## Daftar Modul yang Diimplementasi

### Backend
- `src/backend/csv_manager.py`: Utility untuk operasi file CSV
- `src/backend/feedback_data.py`: Manajemen data feedback
- `src/backend/laporan_data.py`: Manajemen data laporan
- `src/backend/makanan_data.py`: Manajemen data donasi makanan
- `src/backend/request_data.py`: Manajemen data permintaan makanan
- `src/backend/user_data.py`: Manajemen data pengguna
- `src/backend/api/server.py`: Server API utama (Flask)
- `src/backend/api/user_route.py`: Routing API untuk user

### Controller
- `src/controller/account_controller.py`: Logika registrasi & login
- `src/controller/donasi_controller.py`: Logika donasi makanan
- `src/controller/feedback_controller.py`: Logika feedback
- `src/controller/request_controller.py`: Logika permintaan makanan

### Frontend
- `src/frontend/admin_dashboard.py`: Tampilan dashboard admin
- `src/frontend/login_page.py`: Halaman login
- `src/frontend/provider_dashboard.py`: Tampilan dashboard provider
- `src/frontend/receiver_dashboard.py`: Tampilan dashboard receiver
- `src/frontend/register_page.py`: Halaman registrasi
- `src/frontend/side_menu.py`: Komponen menu samping

### Model
- `src/model/feedbackdonasi.py`: Model data feedback
- `src/model/laporandonasi.py`: Model data laporan
- `src/model/makanan.py`: Model data donasi makanan
- `src/model/reqdonasi.py`: Model data permintaan makanan
- `src/model/user.py`: Model data pengguna

