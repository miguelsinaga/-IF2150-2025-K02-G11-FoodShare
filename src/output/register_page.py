import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image
import os

# Fallback import controller
try:
    from src.controller.account_controller import AkunController
except ImportError:
    pass 

class RegisterPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="#DCEE85")
        self.app = app

        # --- Palet Warna ---
        self.colors = {
            "bg_main": "#DCEE85",           # Hijau Lime
            "card_bg": "#FFFFFF",           # Putih (Kartu Kiri)
            "input_bg": "#132A13",          # Hijau Tua Gelap
            "input_fg": "#FFFFFF",          # Teks Input Putih
            "placeholder": "#A0B0A0",       # Placeholder abu-abu
            "btn_bg": "#FFB03B",            # Oranye Tombol
            "btn_hover": "#E5A035",         # Oranye Gelap
            "text_header": "#132A13",       # Judul
            "text_sub": "#556B2F"           # Sub-judul
        }

        # Konfigurasi Grid Utama
        self.grid_columnconfigure(0, weight=1) # Kiri (Kartu Putih)
        self.grid_columnconfigure(1, weight=1) # Kanan (Form)
        self.grid_rowconfigure(0, weight=1)

        # ===========================================================
        # BAGIAN KIRI: Branding (Sama dengan Login)
        # ===========================================================
        self.left_card = ctk.CTkFrame(self, fg_color=self.colors["card_bg"], corner_radius=40)
        self.left_card.grid(row=0, column=0, sticky="nsew", padx=(30, 15), pady=30)
        
        self.left_content = ctk.CTkFrame(self.left_card, fg_color="transparent")
        self.left_content.place(relx=0.5, rely=0.5, anchor="center")

        # Logo
        image_path = "src/assets/logo.png"
        if os.path.exists(image_path):
            pil_image = Image.open(image_path)
            self.logo_image = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(220, 220))
            ctk.CTkLabel(self.left_content, text="", image=self.logo_image).pack(pady=(0, 10))
        else:
            ctk.CTkLabel(self.left_content, text="[LOGO]", font=("Arial", 24)).pack(pady=(0, 10))

        # Teks Branding
        ctk.CTkLabel(self.left_content, text="FoodShare", 
                     font=("Arial", 36, "bold"), text_color="#E89D30").pack(pady=(0, 15))

        # Slogan
        slogan_frame = ctk.CTkFrame(self.left_content, fg_color="transparent")
        slogan_frame.pack()
        ctk.CTkLabel(slogan_frame, text="Share More, ", font=("Arial", 20, "bold"), text_color="#132A13").pack(side="left")
        ctk.CTkLabel(slogan_frame, text="Waste Less", font=("Arial", 20, "bold"), text_color="#A4C639").pack(side="left")

        # ===========================================================
        # BAGIAN KANAN: Form Register
        # ===========================================================
        self.right_panel = ctk.CTkFrame(self, fg_color="transparent")
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=(15, 30), pady=30)

        self.form_container = ctk.CTkFrame(self.right_panel, fg_color="transparent", width=350)
        self.form_container.place(relx=0.5, rely=0.5, anchor="center")

        # 1. Header
        ctk.CTkLabel(self.form_container, text="Join FoodShare!", 
                     font=("Arial", 28, "bold"), text_color=self.colors["text_header"]).pack(pady=(0, 5))
        
        ctk.CTkLabel(self.form_container, text="Create your account", 
                     font=("Arial", 14), text_color=self.colors["text_sub"]).pack(pady=(0, 25))

        # 2. Input Fields (Username, Email, Phone, Password)
        self.nama_entry = self.create_input("Username")
        self.nama_entry.pack(pady=(0, 10))

        self.email_entry = self.create_input("Email")
        self.email_entry.pack(pady=(0, 10))

        # Catatan: Saya menambahkan input No Telepon karena Backend Anda membutuhkannya
        self.phone_entry = self.create_input("Phone Number")
        self.phone_entry.pack(pady=(0, 10))

        self.pass_entry = self.create_input("Password", is_password=True)
        self.pass_entry.pack(pady=(0, 20))

        # 3. Tombol Register (Dua Pilihan Role)
        # Tombol Provider
        self.btn_provider = ctk.CTkButton(
            self.form_container,
            text="Sign Up as Provider",
            font=("Arial", 16, "bold"),
            width=350, height=45,
            corner_radius=10,
            fg_color=self.colors["btn_bg"],
            text_color="#132A13",
            hover_color=self.colors["btn_hover"],
            command=lambda: self.do_register("provider")
        )
        self.btn_provider.pack(pady=(0, 10))

        # Tombol Receiver
        self.btn_receiver = ctk.CTkButton(
            self.form_container,
            text="Sign Up as Receiver",
            font=("Arial", 16, "bold"),
            width=350, height=45,
            corner_radius=10,
            fg_color=self.colors["btn_bg"],
            text_color="#132A13",
            hover_color=self.colors["btn_hover"],
            command=lambda: self.do_register("receiver")
        )
        self.btn_receiver.pack(pady=(0, 20))

        # 4. Footer Login Link
        login_frame = ctk.CTkFrame(self.form_container, fg_color="transparent")
        login_frame.pack()

        ctk.CTkLabel(login_frame, text="Already have an account? ", 
                     font=("Arial", 12), text_color="#556B2F").pack(side="left")
        
        btn_login = ctk.CTkButton(
            login_frame,
            text="login",
            font=("Arial", 12, "bold"),
            fg_color="transparent",
            text_color="#132A13",
            width=40,
            hover=False,
            command=lambda: app.show_frame("LoginPage")
        )
        btn_login.pack(side="left")

    def create_input(self, placeholder, is_password=False):
        return ctk.CTkEntry(
            self.form_container,
            width=350, height=45,
            corner_radius=10,
            fg_color=self.colors["input_bg"],
            text_color=self.colors["input_fg"],
            placeholder_text=placeholder,
            placeholder_text_color=self.colors["placeholder"],
            border_width=0,
            show="*" if is_password else "",
            font=("Arial", 14)
        )

    def do_register(self, role):
        nama = self.nama_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        pw = self.pass_entry.get().strip()

        # Validasi dasar
        if not nama or not email or not pw:
            messagebox.showwarning("Warning", "Mohon lengkapi data (Nama, Email, Password).")
            return

        # Data payload sesuai controller
        data = {
            "nama": nama,
            "email": email,
            "password": pw,
            "noTelepon": phone if phone else "-", # Default strip jika kosong agar tidak error
            "role": role
        }

        try:
            result = AkunController.prosesRegistrasi(data)
            if result["status"] == "SUCCESS":
                messagebox.showinfo("Success", f"Registrasi sebagai {role} berhasil! Silakan login.")
                self.app.show_frame("LoginPage")
            else:
                messagebox.showerror("Error", result["message"])
        except NameError:
            # Mode testing UI
            messagebox.showinfo("Test Mode", f"Register Data:\nRole: {role}\nNama: {nama}\nEmail: {email}")