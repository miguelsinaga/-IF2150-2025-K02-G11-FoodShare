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

        #user_id = repo.next_id()
        user_data = {
            "nama": data["nama"],
            "email": data["email"],
            "password_hash": hash_password(data["password"]),
            "noTelepon": data.get("noTelepon", ""),
            "role": data.get("role", "receiver"),
            "status": "aktif"
        }
        repo.save(user_data)
        new_user = repo.find_by_email(data['email'])
        
        user = Pengguna(**new_user)
        return {"status": "SUCCESS", "message": "Registrasi berhasil", "user": user}

    @staticmethod
    def prosesLogin(email: str, password: str) -> Dict :
        
        user_data = repo.find_by_email(email)

        if not user_data :
            return {"status" : "FAIL","message" : "login gagal" }
        
        user = Pengguna(**user_data)
        if(user.password_hash != hash_password(password)):
            return {"status" : "FAIL" , "message" : "PASSWORD SALAH"}
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
    