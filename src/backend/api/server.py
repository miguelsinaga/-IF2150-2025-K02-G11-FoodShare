from flask import Flask
from .user_route import user_bp

app = Flask(__name__)

# Register Blueprint
app.register_blueprint(user_bp, url_prefix="/api")

print("ROUTES TERDAFTAR:", app.url_map)

if __name__ == "__main__":
    print("API berjalan di 0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000)