from typing import List, Dict
from src.backend.mySQLConnector import get_connection

class FeedbackRepo:
    def ensure_table(self):
        conn = get_connection()
        if conn is None:
            return
        try:
            from src.backend.donatur_data import DonaturRepo
            DonaturRepo().ensure_table()
        except Exception:
            pass
        try:
            from src.backend.penerima_data import PenerimaRepo
            PenerimaRepo().ensure_table()
        except Exception:
            pass
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS feedback (
                id_feedback INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                id_donatur INT,
                id_penerima INT,
                rating INT,
                komentar VARCHAR(100),
                tanggal_feedback DATETIME,
                FOREIGN KEY (id_donatur) REFERENCES donatur(id_user),
                FOREIGN KEY (id_penerima) REFERENCES penerima(id_user)
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
              id_feedback AS idFeedback,
              id_donatur AS idProvider,
              id_penerima AS idReceiver,
              rating,
              komentar,
              tanggal_feedback AS tanggalFeedback
            FROM feedback
            """
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    def find_by_provider(self, provider_id: int) -> List[Dict]:
        conn = get_connection()
        if conn is None:
            return []
        cur = conn.cursor(dictionary=True)
        cur.execute(
            """
            SELECT 
              id_feedback AS idFeedback,
              id_donatur AS idProvider,
              id_penerima AS idReceiver,
              rating,
              komentar,
              tanggal_feedback AS tanggalFeedback
            FROM feedback WHERE id_donatur = %s
            """,
            (provider_id,)
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    def find_by_receiver(self, receiver_id: int) -> List[Dict]:
        conn = get_connection()
        if conn is None:
            return []
        cur = conn.cursor(dictionary=True)
        cur.execute(
            """
            SELECT 
              id_feedback AS idFeedback,
              id_donatur AS idProvider,
              id_penerima AS idReceiver,
              rating,
              komentar,
              tanggal_feedback AS tanggalFeedback
            FROM feedback WHERE id_penerima = %s
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
        cur.execute("SELECT COALESCE(MAX(id_feedback), 0) + 1 FROM feedback")
        row = cur.fetchone()
        cur.close()
        conn.close()
        return int(row[0]) if row and row[0] is not None else 1

    def save(self, fb: Dict):
        self.ensure_table()
        conn = get_connection()
        if conn is None:
            return
        cur = conn.cursor()
        sql = (
            "INSERT INTO feedback (id_feedback, id_donatur, id_penerima, rating, komentar, tanggal_feedback) "
            "VALUES (%s, %s, %s, %s, %s, %s)"
        )
        values = (
            fb["idFeedback"],
            fb["idProvider"],
            fb["idReceiver"],
            fb["rating"],
            fb.get("komentar", ""),
            fb.get("tanggalFeedback", "")
        )
        cur.execute(sql, values)
        conn.commit()
        cur.close()
        conn.close()

    def update(self, fb: Dict):
        self.ensure_table()
        conn = get_connection()
        if conn is None:
            return
        cur = conn.cursor()
        sql = (
            "UPDATE feedback SET id_donatur=%s, id_penerima=%s, rating=%s, komentar=%s, tanggal_feedback=%s WHERE id_feedback=%s"
        )
        values = (
            fb["idProvider"],
            fb["idReceiver"],
            fb["rating"],
            fb.get("komentar", ""),
            fb.get("tanggalFeedback", ""),
            fb["idFeedback"]
        )
        cur.execute(sql, values)
        conn.commit()
        cur.close()
        conn.close()
