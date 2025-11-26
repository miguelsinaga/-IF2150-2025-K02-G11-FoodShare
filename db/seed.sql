USE foodshare;

INSERT INTO users (nama, email, password_hash, noTelepon, role, status) VALUES
('Provider Satu','provider@example.com','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','081234567890','provider','aktif'),
('Receiver Satu','receiver@example.com','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','089876543210','receiver','aktif'),
('Admin Sistem','admin@example.com','8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92','080000000000','admin','aktif');

INSERT INTO donatur (id_user, total_donasi, status_akun)
SELECT id, 0, 'aktif' FROM users WHERE role = 'provider' AND email = 'provider@example.com';

INSERT INTO penerima (id_user, alamat)
SELECT id, 'Jl. Contoh No. 1' FROM users WHERE role = 'receiver' AND email = 'receiver@example.com';

INSERT INTO makanan (id_donatur, jenis_makanan, jumlah_porsi, lokasi, batas_waktu, status)
VALUES (
  (SELECT id FROM users WHERE email = 'provider@example.com'),
  'Roti Tawar', 20, 'Jl. Mawar 1', '2025-12-31', 'Tersedia'
);
