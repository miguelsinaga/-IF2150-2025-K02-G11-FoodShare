# src/repository/pengguna_repo.py
from typing import Optional, List, Dict
from .csv_manager import CSVManager
import os

BASE_DIR = os.path.join(os.getcwd(), "data")
USERS_CSV = os.path.join(BASE_DIR, "users.csv")

_user_header = ["id","nama","email","password_hash","noTelepon","role","status"]

class User:
    def __init__(self, path: str = USERS_CSV):
        self._mgr = CSVManager(path, _user_header)

    def all(self) -> List[Dict]:
        rows = self._mgr.read_all()
        res = []
        for r in rows[1:]:
            res.append({
                "id": int(r[0]),
                "nama": r[1],
                "email": r[2],
                "password_hash": r[3],
                "noTelepon": r[4],
                "role": r[5],
                "status": r[6]
            })
        return res

    def find_by_email(self, email: str) -> Optional[Dict]:
        for u in self.all():
            if u["email"].lower() == email.lower():
                return u
        return None

    def find_by_id(self, uid: int) -> Optional[Dict]:
        for u in self.all():
            if u["id"] == uid:
                return u
        return None

    def next_id(self) -> int:
        return self._mgr.next_id()

    def save(self, user: Dict):
        row = [user["id"], user["nama"], user["email"], user["password_hash"], user.get("noTelepon",""), user.get("role","receiver"), user.get("status","aktif")]
        self._mgr.append_row(row)

    def update(self, user: Dict):
        rows = self._mgr.read_all()
        header = rows[0]
        new = [header]
        for r in rows[1:]:
            if int(r[0]) == int(user["id"]):
                new.append([user["id"], user["nama"], user["email"], user["password_hash"], user.get("noTelepon",""), user.get("role","receiver"), user.get("status","aktif")])
            else:
                new.append(r)
        self._mgr.write_all(new)
