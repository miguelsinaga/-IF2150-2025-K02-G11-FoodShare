# src/model/pengguna.py
from dataclasses import dataclass
from typing import Optional
from src.backend.user_data import UserRepo

repo = UserRepo()

@dataclass
class Pengguna:
    id: int
    nama: str
    email: str
    password_hash: str
    noTelepon: str
    role: str
    status: str = "aktif"

    @staticmethod
    def from_dict(d: dict) -> "Pengguna":
        return Pengguna(
            id=d["id"],
            nama=d["nama"],
            email=d["email"],
            password_hash=d["password_hash"],
            noTelepon=d["noTelepon"],
            role=d["role"],
            status=d["status"],
        )

    @staticmethod
    def find_by_email(email: str) -> Optional["Pengguna"]:
        raw = repo.find_by_email(email)
        return Pengguna.from_dict(raw) if raw else None

    @staticmethod
    def find_by_id(uid: int) -> Optional["Pengguna"]:
        raw = repo.find_by_id(uid)
        return Pengguna.from_dict(raw) if raw else None

    @staticmethod
    def all():
        return [Pengguna.from_dict(u) for u in repo.all()]

    def save(self):
        repo.save({
            "id": self.id,
            "nama": self.nama,
            "email": self.email,
            "password_hash": self.password_hash,
            "noTelepon": self.noTelepon,
            "role": self.role,
            "status": self.status
        })

    def update(self):
        repo.update({
            "id": self.id,
            "nama": self.nama,
            "email": self.email,
            "password_hash": self.password_hash,
            "noTelepon": self.noTelepon,
            "role": self.role,
            "status": self.status
        })
