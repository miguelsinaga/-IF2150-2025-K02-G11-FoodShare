import requests
import socket

# Ubah ini ke IP server kamu

API_BASE = "https://tabescent-kymberly-frugally.ngrok-free.dev/api"

def api_login(email, password):
    url = f"{API_BASE}/login"

    payload = {
        "email": email,
        "password": password
    }

    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        return {"status":"ERROR", "message": f"Tidak bisa konek ke API: {e}"}

def api_register(nama,email,password,noTelepon,role):
    url = f"{API_BASE}/register"
    print("REGISTER URL:", url) 
    payload = {
        "nama":nama,
        "email": email,
        "password": password,
        "noTelepon":noTelepon,
        "role":role
    }

    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        return {"status":"ERROR", "message": f"Tidak bisa konek ke API: {e}"}


def api_forgot_password(email,noTelepon,password):
    url = f"{API_BASE}/forgot-password"
    payload = {
        "email" :email,
        "noTelepon" : noTelepon,
        "password" : password 
    }

    try :
        response = requests.post(url,json=payload)
        return response.json()
    except Exception as e:
        return {"status":"ERROR","message":f"Tidak bisa konek ke API : {e}"}