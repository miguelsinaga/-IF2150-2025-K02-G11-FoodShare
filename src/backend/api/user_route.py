from flask import Blueprint, request, jsonify
from src.controller.account_controller import AkunController

user_bp = Blueprint("user_bp", __name__)

@user_bp.post("/login")
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    result = AkunController.prosesLogin(email, password)

    # Convert class Pengguna → dict agar aman dikirim via JSON
    if result["status"] == "SUCCESS":
        user = result["user"]
        user_dict = {
            "id": user["id"],
            "nama": user["nama"],
            "email": user["email"],
            "password_hash": user["password_hash"],
            "noTelepon": user["noTelepon"],
            "role": user["role"],
            "status": user["status"]
        }
        return jsonify({"status":"SUCCESS","user":user_dict})

    return jsonify(result)

@user_bp.post("/register")
def register():
    print(">>> REGISTER ROUTE TERIMA REQUEST <<<")
    print("RAW DATA:", request.data)
    print("JSON:", request.get_json(silent=True))

    data = request.get_json()
    nama = data.get("nama")
    email = data.get("email")
    password = data.get("password")
    noTelepon = data.get("noTelepon")
    role = data.get("role")

    new_user_dict = {
        "nama": nama,
        "email": email,
        "password": password,
        "noTelepon": noTelepon,
        "role": role,
        "status": "aktif"
    }

    result = AkunController.prosesRegistrasi(new_user_dict)
    if result["status"] == "SUCCESS":
        user = result["user"]
        user_dict = {
            "id": user.id,
            "nama": user.nama,
            "email": user.email,
            "password_hash": user.password_hash,
            "noTelepon": user.noTelepon,
            "role": user.role,
            "status": user.status
        }
        return jsonify({"status":"SUCCESS","user":user_dict})
    return jsonify(result)

@user_bp.post("/forgot-password")
def forgotpassword():
    data = request.get_json()
    email = data.get("email")
    noTelepon = data.get("noTelepon")
    password = data.get("password")

    result = AkunController.LupaPassword(email,noTelepon,password)

    if(result["status"] == "SUCCESS"):
        return jsonify({"status":"SUCCESS","user":result["user"]})
    return jsonify(result)
