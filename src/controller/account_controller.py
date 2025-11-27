import hashlib
from typing import Dict
from src.model.user import Pengguna
from src.backend.user_data import UserRepo
from flask import Flask, request, jsonify
repo = UserRepo()

def hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode("utf-8")).hexdigest()

class AkunController:
    @staticmethod
    def validasiInput(data: Dict) -> Dict:
        nama = str(data.get("nama", "")).strip()
        email = str(data.get("email", "")).strip()
        password = str(data.get("password", ""))
        role = str(data.get("role", "receiver")).strip()
        if not nama or not email or not password:
            return {"status": "FAIL", "message": "Data tidak lengkap"}
        if "@" not in email:
            return {"status": "FAIL", "message": "Email tidak valid"}
        if len(password) < 6:
            return {"status": "FAIL", "message": "Password terlalu pendek"}
        if role not in ["provider", "receiver", "admin"]:
            return {"status": "FAIL", "message": "Role tidak valid"}
        return {"status": "SUCCESS"}

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
        v = AkunController.validasiInput(data)
        if v.get("status") != "SUCCESS":
            return v
        
        email_norm = data["email"].strip().lower()
        if repo.find_by_email(email_norm):
            return {"status": "FAIL", "message": "Email sudah terdaftar"}

        #user_id = repo.next_id()
        user_data = {
            "nama": data["nama"],
            "email": email_norm,
            "password_hash": hash_password(data["password"]),
            "noTelepon": data.get("noTelepon", ""),
            "role": data.get("role", "receiver"),
            "status": "aktif"
        }
        repo.save(user_data)
        new_user = repo.find_by_email(email_norm)
        
        user = Pengguna(**new_user)
        return {"status": "SUCCESS", "message": "Registrasi berhasil", "user": user}

    @staticmethod
    def prosesLogin(email: str, password: str) -> Dict :
        
        user_data = repo.find_by_email(email.strip().lower())

        if not user_data :
            return {"status" : "FAIL","message" : "login gagal" }
        
        user = Pengguna(**user_data)
        if(user.password_hash != hash_password(password)):
            return {"status" : "FAIL" , "message" : "PASSWORD SALAH"}
        # Cegah login jika provider diblokir via DonaturRepo
        try:
            if user.role == "provider":
                from src.backend.donatur_data import DonaturRepo
                dr = DonaturRepo().find_by_user_id(user.id)
                if dr and str(dr.get("status_akun","aktif")).lower() != "aktif":
                    return {"status": "FAIL", "message": "Akun provider Anda diblokir oleh admin."}
        except Exception:
            pass
        if str(user.status).lower() == "banned":
            return {"status": "FAIL", "message": "Akun Anda diblokir dan tidak dapat login."}
        user_dict = {
            "id": user.id,
            "nama": user.nama,
            "email": user.email,
            "password_hash": user.password_hash,
            "noTelepon": user.noTelepon,
            "role": user.role,
            "status": user.status
        }
        return {"status" : "SUCCESS","message" : "login berhasil" ,"user":user_dict}
    
    def LupaPassword(email: str, noTelepon: str, new_pass : str) -> Dict :
        user_data = repo.find_by_email(email)
        if not user_data : 
            return {"status" : "FAIL", "message" : "Tidak ada email"}
        
        user = Pengguna(**user_data)
        if(user.noTelepon != noTelepon):
            return {"status" : "FAIL", "message" : "Nomor Telepon tidak sesuai"}
        
        repo.update_password(user,hash_password(new_pass))

        new_pass = repo.find_by_email(email)

        user = Pengguna(**new_pass)
        user_dict = {
            "id": user.id,
            "nama": user.nama,
            "email": user.email,
            "password_hash": user.password_hash,
            "noTelepon": user.noTelepon,
            "role": user.role,
            "status": user.status
        }
        return {"status":"SUCCESS","message" : "Password baru akan diproses","user":user_dict}
    
