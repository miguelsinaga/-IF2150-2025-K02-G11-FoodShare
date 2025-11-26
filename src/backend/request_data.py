from typing import List, Dict, Optional
from src.backend.mySQLConnector import get_connection

class RequestRepo:
    def ensure_table(self):
        conn = get_connection()
        if conn is None:
            return
        try:
            from src.backend.penerima_data import PenerimaRepo
            PenerimaRepo().ensure_table()
        except Exception:
            pass
        try:
            from src.backend.makanan_data import DataMakananRepo
            DataMakananRepo().ensure_table()
        except Exception:
            pass
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS request_donasi (
                id_request INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                id_penerima INT,
                id_makanan INT,
                status VARCHAR(15) DEFAULT 'aktif',
                tanggal_request DATETIME,
                FOREIGN KEY (id_penerima) REFERENCES penerima(id_user),
                FOREIGN KEY (id_makanan) REFERENCES makanan(id_makanan)
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
              id_request AS idRequest,
              id_makanan AS idDonasi,
              id_penerima AS idReceiver,
              status,
              tanggal_request AS tanggalRequest
            FROM request_donasi
            """
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    def find_by_id(self, idRequest: int) -> Optional[Dict]:
        self.ensure_table()
        conn = get_connection()
        if conn is None:
            return None
        cur = conn.cursor(dictionary=True)
        cur.execute(
            """
            SELECT 
              id_request AS idRequest,
              id_makanan AS idDonasi,
              id_penerima AS idReceiver,
              status,
              tanggal_request AS tanggalRequest
            FROM request_donasi WHERE id_request = %s
            """,
            (idRequest,)
        )
        row = cur.fetchone()
        cur.close()
        conn.close()
        return row

    def find_by_receiver(self, receiver_id: int) -> List[Dict]:
        self.ensure_table()
        conn = get_connection()
        if conn is None:
            return []
        cur = conn.cursor(dictionary=True)
        cur.execute(
            """
            SELECT 
              id_request AS idRequest,
              id_makanan AS idDonasi,
              id_penerima AS idReceiver,
              status,
              tanggal_request AS tanggalRequest
            FROM request_donasi WHERE id_penerima = %s
            """,
            (receiver_id,)
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
        cur.execute("SELECT COALESCE(MAX(id_request), 0) + 1 FROM request_donasi")
        row = cur.fetchone()
        cur.close()
        conn.close()
        return int(row[0]) if row and row[0] is not None else 1

    def save(self, req: Dict):
        self.ensure_table()
        conn = get_connection()
        if conn is None:
            return
        cur = conn.cursor()
        sql = (
            "INSERT INTO request_donasi (id_request, id_makanan, id_penerima, status, tanggal_request) "
            "VALUES (%s, %s, %s, %s, %s)"
        )
        values = (
            req["idRequest"],
            req["idDonasi"],
            req["idReceiver"],
            req.get("status", "Pending"),
            req.get("tanggalRequest", "")
        )
        cur.execute(sql, values)
        conn.commit()
        cur.close()
        conn.close()

    def update(self, req: Dict):
        self.ensure_table()
        conn = get_connection()
        if conn is None:
            return
        cur = conn.cursor()
        sql = (
            "UPDATE request_donasi SET id_makanan=%s, id_penerima=%s, status=%s, tanggal_request=%s WHERE id_request=%s"
        )
        values = (
            req["idDonasi"],
            req["idReceiver"],
            req.get("status", "Pending"),
            req.get("tanggalRequest", ""),
            req["idRequest"]
        )
        cur.execute(sql, values)
        conn.commit()
        cur.close()
        conn.close()
