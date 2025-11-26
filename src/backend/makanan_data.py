from typing import List, Dict, Optional
from src.backend.mySQLConnector import get_connection

class DataMakananRepo:
    def ensure_table(self):
        conn = get_connection()
        if conn is None:
            return
        try:
            from src.backend.donatur_data import DonaturRepo
            DonaturRepo().ensure_table()
        except Exception:
            pass
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS makanan (
                id_makanan INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                id_donatur INT,
                jenis_makanan VARCHAR(40),
                jumlah_porsi INT,
                lokasi VARCHAR(40),
                batas_waktu DATETIME,
                status VARCHAR(10) DEFAULT 'layak',
                FOREIGN KEY (id_donatur) REFERENCES donatur(id_user)
            )
            """
        )
        conn.commit()
        cur.close()
        conn.close()
    def all(self) -> List[Dict]:
        self.ensure_table()
        conn = get_connection()
        if conn is None:
            return []
        cur = conn.cursor(dictionary=True)
        cur.execute(
            """
            SELECT 
              id_makanan AS idDonasi,
              id_donatur AS idProvider,
              jenis_makanan AS jenisMakanan,
              jumlah_porsi AS jumlahPorsi,
              lokasi,
              batas_waktu AS batasWaktu,
              status,
              '' AS tanggal_donasi
            FROM makanan
            """
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    def find_by_id(self, idDonasi: int) -> Optional[Dict]:
        self.ensure_table()
        conn = get_connection()
        if conn is None:
            return None
        cur = conn.cursor(dictionary=True)
        cur.execute(
            """
            SELECT 
              id_makanan AS idDonasi,
              id_donatur AS idProvider,
              jenis_makanan AS jenisMakanan,
              jumlah_porsi AS jumlahPorsi,
              lokasi,
              batas_waktu AS batasWaktu,
              status,
              '' AS tanggal_donasi
            FROM makanan WHERE id_makanan = %s
            """,
            (idDonasi,)
        )
        row = cur.fetchone()
        cur.close()
        conn.close()
        return row

    def find_by_status(self, status: str) -> List[Dict]:
        self.ensure_table()
        conn = get_connection()
        if conn is None:
            return []
        cur = conn.cursor(dictionary=True)
        cur.execute(
            """
            SELECT 
              id_makanan AS idDonasi,
              id_donatur AS idProvider,
              jenis_makanan AS jenisMakanan,
              jumlah_porsi AS jumlahPorsi,
              lokasi,
              batas_waktu AS batasWaktu,
              status,
              '' AS tanggal_donasi
            FROM makanan WHERE status = %s
            """,
            (status,)
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    def find_by_provider(self, provider_id: int) -> List[Dict]:
        self.ensure_table()
        conn = get_connection()
        if conn is None:
            return []
        cur = conn.cursor(dictionary=True)
        cur.execute(
            """
            SELECT 
              id_makanan AS idDonasi,
              id_donatur AS idProvider,
              jenis_makanan AS jenisMakanan,
              jumlah_porsi AS jumlahPorsi,
              lokasi,
              batas_waktu AS batasWaktu,
              status,
              '' AS tanggal_donasi
            FROM makanan WHERE id_donatur = %s
            """,
            (provider_id,)
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    def next_id(self) -> int:
        self.ensure_table()
        conn = get_connection()
        if conn is None:
            return 1
        cur = conn.cursor()
        cur.execute("SELECT COALESCE(MAX(id_makanan), 0) + 1 FROM makanan")
        row = cur.fetchone()
        cur.close()
        conn.close()
        return int(row[0]) if row and row[0] is not None else 1

    def save(self, data: Dict):
        self.ensure_table()
        conn = get_connection()
        if conn is None:
            return
        cur = conn.cursor()
        sql = (
            "INSERT INTO makanan (id_makanan, id_donatur, jenis_makanan, jumlah_porsi, lokasi, batas_waktu, status) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)"
        )
        values = (
            data["idDonasi"],
            data["idProvider"],
            data["jenisMakanan"],
            data["jumlahPorsi"],
            data["lokasi"],
            data["batasWaktu"],
            data.get("status", "layak")
        )
        cur.execute(sql, values)
        conn.commit()
        cur.close()
        conn.close()

    def update(self, data: Dict):
        self.ensure_table()
        conn = get_connection()
        if conn is None:
            return
        cur = conn.cursor()
        sql = (
            "UPDATE makanan SET id_donatur=%s, jenis_makanan=%s, jumlah_porsi=%s, lokasi=%s, batas_waktu=%s, status=%s WHERE id_makanan=%s"
        )
        values = (
            data["idProvider"],
            data["jenisMakanan"],
            data["jumlahPorsi"],
            data["lokasi"],
            data["batasWaktu"],
            data.get("status", "layak"),
            data["idDonasi"]
        )
        cur.execute(sql, values)
        conn.commit()
        cur.close()
        conn.close()

    def delete(self, idDonasi: int):
        self.ensure_table()
        conn = get_connection()
        if conn is None:
            return
        cur = conn.cursor()
        cur.execute("DELETE FROM makanan WHERE id_makanan = %s", (idDonasi,))
        conn.commit()
        cur.close()
        conn.close()
