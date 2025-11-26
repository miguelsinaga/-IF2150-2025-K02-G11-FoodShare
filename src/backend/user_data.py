# src/backend/user_data.py

import os
import csv
from typing import List, Dict, Optional
from flask import Flask, request, jsonify
import mysql.connector
from src.backend.mySQLConnector import get_connection
# ========================
#  CSV Manager (SAFE)
# ========================

class CSVManager:
    def __init__(self, filepath: str, header: List[str]):
        self.filepath = filepath
        self.header = header

        # Pastikan folder data ada
        base_folder = os.path.dirname(filepath)
        if not os.path.exists(base_folder):
            os.makedirs(base_folder)

        # Jika CSV tidak ada → buat baru
        if not os.path.exists(filepath):
            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(header)

    def read_all(self) -> List[List[str]]:
        try:
            with open(self.filepath, "r", newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                return list(reader)
        except Exception as e:
            print("CSV READ ERROR:", e)
            return []

    def write_all(self, rows: List[List[str]]):
        with open(self.filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(rows)

    def append_row(self, row: List[str]):
        with open(self.filepath, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(row)

    def next_id(self) -> int:
        rows = self.read_all()
        try:
            last = int(rows[-1][0])
            return last + 1
        except:
            return 1


# =======================================
#   SAFE PATH → Tidak Tergantung cwd
# =======================================

# __file__ = .../src/backend/user_data.py
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # naik 3 folder
BASE_DIR = os.path.join(ROOT, "data")
USERS_CSV = os.path.join(BASE_DIR, "users.csv")

_user_header = ["id", "nama", "email", "password_hash",
                "noTelepon", "role", "status"]


# =========================
#  USER REPOSITORY (SAFE)
# =========================

# class UserRepo:
#     def __init__(self, path: str = USERS_CSV):
#         self._mgr = CSVManager(path, _user_header)

#     # ------ Baca semua user ------
#     def all(self) -> List[Dict]:
#         rows = self._mgr.read_all()
#         users = []

#         # Debug opsional
#         # print("DEBUG RAW CSV:", rows)

#         for r in rows[1:]:  # skip header

#             # Skip row kosong atau kurang kolom
#             if not r or len(r) < 7:
#                 continue

#             # Trim semua whitespace
#             r = [col.strip() for col in r]

#             try:
#                 users.append({
#                     "id": int(r[0]),
#                     "nama": r[1],
#                     "email": r[2],
#                     "password_hash": r[3],
#                     "noTelepon": r[4],
#                     "role": r[5],
#                     "status": r[6]
#                 })
#             except Exception as e:
#                 print("SKIP BAD ROW:", r, "ERROR:", e)
#                 continue

#         return users

#     # ------ Cari berdasarkan email ------
#     def find_by_email(self, email: str) -> Optional[Dict]:
#         email = email.strip().lower()

#         for u in self.all():
#             if u["email"].lower() == email:
#                 return u
#         return None

#     # ------ Cari berdasarkan id ------
#     def find_by_id(self, uid: int) -> Optional[Dict]:
#         for u in self.all():
#             if u["id"] == uid:
#                 return u
#         return None

#     # ------ Insert user baru ------
#     def save(self, user: Dict):
#         row = [
#             user["id"],
#             user["nama"],
#             user["email"],
#             user["password_hash"],
#             user.get("noTelepon", ""),
#             user.get("role", "receiver"),
#             user.get("status", "aktif"),
#         ]
#         self._mgr.append_row(row)

#     # ------ Update user ------
#     def update(self, user: Dict):
#         rows = self._mgr.read_all()
#         header = rows[0]
#         new = [header]

#         for r in rows[1:]:
#             if len(r) < 7:
#                 continue

#             if int(r[0]) == int(user["id"]):
#                 new.append([
#                     user["id"],
#                     user["nama"],
#                     user["email"],
#                     user["password_hash"],
#                     user.get("noTelepon", ""),
#                     user.get("role", "receiver"),
#                     user.get("status", "aktif")
#                 ])
#             else:
#                 new.append(r)

#         self._mgr.write_all(new)

class UserRepo :
    def all(self) -> List[Dict]:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")

        data = cursor.fetchall()

        cursor.close()
        conn.close()

        return data
    
    def find_by_email(self,email:str) -> Optional[Dict]:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE email = %s",(email,))

        user = cursor.fetchone()
        cursor.close()
        conn.close()
        print("print Database \n : ",user)
        return user
    
    def find_by_id(self,id:int) -> Optional[Dict]:
        data = request.json
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE id = %d",(data["id"],))

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        return user
    
    def save(self, user: Dict):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            INSERT INTO users (nama, email, password_hash, noTelepon, role, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            user["nama"],
            user["email"],
            user["password_hash"],
            user.get("noTelepon", ""),
            user.get("role", "receiver"),
            user.get("status", "aktif")
        )

        cursor.execute(sql, values)
        conn.commit()

        cursor.close()
        conn.close()

    # Update user
    def update(self, user: Dict):
        conn = get_connection()
        if conn is None:
            raise Exception("Cannot connect to MySQL server. Please ensure MySQL is running.")
        
        cursor = conn.cursor()

        sql = """
            UPDATE users SET
                nama = %s,
                email = %s,
                password_hash = %s,
                noTelepon = %s,
                role = %s,
                status = %s
            WHERE id = %s
        """

        values = (
            user["nama"],
            user["email"],
            user["password_hash"],
            user.get("noTelepon", ""),
            user.get("role", "receiver"),
            user.get("status", "aktif"),
            user["id"]
        )

        cursor.execute(sql, values)
        conn.commit()

        cursor.close()
        conn.close()

    def update_password(self,user:Dict,new_pass:str):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            UPDATE users SET
                password_hash = %s
            WHERE email = %s
        """
        
        values = (
            new_pass,
            user.email
        )

        cursor.execute(sql, values)
        conn.commit()

        cursor.close()
        conn.close()