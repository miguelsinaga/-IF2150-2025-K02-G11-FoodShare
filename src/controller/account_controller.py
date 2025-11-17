import hashlib
from typing import Dict
from src.model.user import Pengguna
from src.backend.user_data import User

repo = User()

def hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode("utf-8")).hexdigest()

class AkunController:

    @staticmethod
    def prosesRegistrasi(data: Dict) -> Dict:
        """
        data = {
            "nama": ...,
            "email": ...,
            "password": ...,
            "noTelepon": ...,
            "role": "provider/receiver/admin"
        }
        """
        # Cek email duplikat
        if repo.find_by_email(data["email"]):
            return {"status": "FAIL", "message": "Email sudah terdaftar"}

        user_id = repo.next_id()

        user = Pengguna(
            id=user_id,
            nama=data["nama"],
            email=data["email"],
            password_hash=hash_password(data["password"]),
            noTelepon=data["noTelepon"],
            role=data["role"],
            status="aktif"
        )

        user.save()
        return {"status": "SUCCESS", "message": "Registrasi berhasil", "user": user}

    @staticmethod
    def prosesLogin(email: str, password: str) -> Dict:
        user = Pengguna.find_by_email(email)
        if not user:
            return {"status": "FAIL", "message": "Email tidak terdaftar"}

        if user.password_hash != hash_password(password):
            return {"status": "FAIL", "message": "Password salah"}

        return {"status": "SUCCESS", "message": "Login berhasil", "user": user}
