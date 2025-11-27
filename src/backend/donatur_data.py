from typing import Optional
from src.backend.mySQLConnector import get_connection

class DonaturRepo:
    def ensure_table(self):
        conn = get_connection()
        if conn is None:
            return
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS donatur (
                id_user INT PRIMARY KEY,
                total_donasi INT,
                status_akun VARCHAR(15) DEFAULT 'aktif',
                FOREIGN KEY (id_user) REFERENCES users(id)
            )
            """
        )
        conn.commit()
        cur.close()
        conn.close()

    def find_by_user_id(self, user_id: int) -> Optional[dict]:
        conn = get_connection()
        if conn is None:
            return None
        cur = conn.cursor(dictionary=True)
        try:
            cur.execute("SELECT id_user, total_donasi, status_akun FROM donatur WHERE id_user = %s", (user_id,))
        except Exception:
            cur.close()
            conn.close()
            self.ensure_table()
            conn = get_connection()
            if conn is None:
                return None
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT id_user, total_donasi, status_akun FROM donatur WHERE id_user = %s", (user_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return row

    def ensure_exists(self, user_id: int):
        self.ensure_table()
        if self.find_by_user_id(user_id):
            return
        conn = get_connection()
        if conn is None:
            return
        cur = conn.cursor()
        cur.execute("INSERT INTO donatur (id_user, total_donasi, status_akun) VALUES (%s, %s, %s)", (user_id, 0, "aktif"))
        conn.commit()
        cur.close()
        conn.close()

    def update_status(self, user_id: int, status: str):
        self.ensure_table()
        conn = get_connection()
        if conn is None:
            return
        cur = conn.cursor()
        cur.execute("UPDATE donatur SET status_akun=%s WHERE id_user=%s", (status, user_id))
        conn.commit()
        cur.close()
        conn.close()
