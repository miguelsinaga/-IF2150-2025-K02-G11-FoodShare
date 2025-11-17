"""Seed initial data into `data/` CSV files.
Run: python scripts/seed.py
This script will create `data/` and write default users/donasi entries.
"""
import os
import csv
import hashlib

ROOT = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT, "data")
os.makedirs(DATA_DIR, exist_ok=True)

USERS_CSV = os.path.join(DATA_DIR, "users.csv")
DONASI_CSV = os.path.join(DATA_DIR, "donasi.csv")
REQUESTS_CSV = os.path.join(DATA_DIR, "requests.csv")
FEEDBACK_CSV = os.path.join(DATA_DIR, "feedback.csv")
LAPORAN_CSV = os.path.join(DATA_DIR, "laporan.csv")

def sha256(pw: str) -> str:
    return hashlib.sha256(pw.encode('utf-8')).hexdigest()

# Users
users_header = ["id","nama","email","password_hash","noTelepon","role","status"]
users = [
    [1, "Miguel", "miguel@gmail.com", sha256("123456"), "08123456", "provider", "aktif"],
    [2, "Provider Satu", "provider@example.com", sha256("123456"), "081234567890", "provider", "aktif"],
    [3, "Receiver Satu", "receiver@example.com", sha256("123456"), "089876543210", "receiver", "aktif"],
    [4, "Admin Sistem", "admin@example.com", sha256("123456"), "080000000000", "admin", "aktif"],
]

# Donasi
donasi_header = ["idDonasi","idProvider","jenisMakanan","jumlahPorsi","lokasi","batasWaktu","status","tanggal_donasi"]
# keep empty by default

def write_csv(path, header, rows):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for r in rows:
            writer.writerow(r)
    print('Wrote', path)

# Only seed users if file is missing or has only header
if not os.path.exists(USERS_CSV):
    write_csv(USERS_CSV, users_header, users)
else:
    with open(USERS_CSV, 'r', encoding='utf-8') as f:
        lines = [l for l in f.read().splitlines() if l.strip()]
    if len(lines) <= 1:
        write_csv(USERS_CSV, users_header, users)
    else:
        print('Users CSV exists and contains data; skipping')

# Ensure donasi/request/feedback/laporan exist with header
for path, header in [
    (DONASI_CSV, donasi_header),
    (REQUESTS_CSV, ["idRequest","idDonasi","idReceiver","status","tanggalRequest"]),
    (FEEDBACK_CSV, ["idFeedback","idProvider","idReceiver","rating","komentar","tanggalFeedback"]),
    (LAPORAN_CSV, ["idLaporan","idRequest","tanggalLaporan","jenisLaporan","deskripsi","estimasiPengurangan"]) 
]:
    if not os.path.exists(path):
        write_csv(path, header, [])
    else:
        with open(path, 'r', encoding='utf-8') as f:
            lines = [l for l in f.read().splitlines() if l.strip()]
        if len(lines) <= 1:
            write_csv(path, header, [])
        else:
            print(path, 'already has data; skipping')

print('Seeding complete')
