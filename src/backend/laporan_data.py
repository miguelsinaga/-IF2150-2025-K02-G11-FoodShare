from typing import List, Dict
from src.backend.mySQLConnector import get_connection

class LaporanRepo:
    def ensure_table(self):
        conn = get_connection()
        if conn is None:
            return
        try:
            from src.backend.request_data import RequestRepo
            RequestRepo().ensure_table()
        except Exception:
            pass
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS laporan_donasi (
                id_laporan INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                id_request INT,
                tanggal_laporan DATETIME,
                jenis_laporan VARCHAR(30),
                deskripsi VARCHAR(100),
                bukti VARCHAR(50),
                estimasi_pengurangan DECIMAL(10,2),
                FOREIGN KEY (id_request) REFERENCES request_donasi(id_request)
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
              id_laporan AS idLaporan,
              id_request AS idRequest,
              tanggal_laporan AS tanggalLaporan,
              jenis_laporan AS jenisLaporan,
              deskripsi,
              estimasi_pengurangan AS estimasiPengurangan
            FROM laporan_donasi
            """
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
        cur.execute("SELECT COALESCE(MAX(id_laporan), 0) + 1 FROM laporan_donasi")
        row = cur.fetchone()
        cur.close()
        conn.close()
        return int(row[0]) if row and row[0] is not None else 1

    def save(self, lap: Dict):
        self.ensure_table()
        conn = get_connection()
        if conn is None:
            return
        cur = conn.cursor()
        sql = (
            "INSERT INTO laporan_donasi (id_laporan, id_request, tanggal_laporan, jenis_laporan, deskripsi, estimasi_pengurangan) "
            "VALUES (%s, %s, %s, %s, %s, %s)"
        )
        values = (
            lap["idLaporan"],
            lap["idRequest"],
            lap.get("tanggalLaporan", ""),
            lap.get("jenisLaporan", ""),
            lap.get("deskripsi", ""),
            lap.get("estimasiPengurangan", 0.0)
        )
        cur.execute(sql, values)
        conn.commit()
        cur.close()
        conn.close()
