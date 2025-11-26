import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image
import os
from src.backend.api.client_api import api_forgot_password
# Fallback import controller
try:
    from src.controller.account_controller import AkunController
except ImportError:
    pass 

class ForgotPassword(ctk.CTkFrame):
    def __init__(self, parent, app):
        # Set warna background utama menjadi Hijau Lime (#DCEE85)
        super().__init__(parent, fg_color="#DCEE85")
        self.app = app
        
        # --- Palet Warna ---
        self.colors = {
            "bg_main": "#DCEE85",           # Hijau Lime (Background Utama)
            "card_bg": "#FFFFFF",           # Putih (Kartu Kiri)
            "input_bg": "#132A13",          # Hijau Tua Gelap (Input Field)
            "input_fg": "#FFFFFF",          # Teks Input Putih
            "placeholder": "#A0B0A0",       # Placeholder abu-abu
            "btn_bg": "#FFB03B",            # Oranye Tombol
            "btn_hover": "#E5A035",         # Oranye Gelap (Hover)
            "text_header": "#132A13",       # Teks Header
            "text_sub": "#556B2F"           # Teks Sub-header
        }

        # Konfigurasi Grid Utama agar FULL SCREEN / Responsive
        self.grid_columnconfigure(0, weight=1) # Kiri (Kartu Putih)
        self.grid_columnconfigure(1, weight=1) # Kanan (Form)
        self.grid_rowconfigure(0, weight=1)

        # ===========================================================
        # BAGIAN KIRI: Floating White Card
        # ===========================================================
        self.left_card = ctk.CTkFrame(
            self, 
            fg_color=self.colors["card_bg"], 
            corner_radius=40 
        )
        self.left_card.grid(row=0, column=0, sticky="nsew", padx=(30, 15), pady=30)
        
        # Frame internal untuk menengahkan konten logo
        self.left_content = ctk.CTkFrame(self.left_card, fg_color="transparent")
        self.left_content.place(relx=0.5, rely=0.5, anchor="center")

        # 1. Logo Image
        image_path = "src/assets/logo.png"
        if os.path.exists(image_path):
            pil_image = Image.open(image_path)
            self.logo_image = ctk.CTkImage(light_image=pil_image, 
                                           dark_image=pil_image, 
                                           size=(220, 220)) 
            ctk.CTkLabel(self.left_content, text="", image=self.logo_image).pack(pady=(0, 10))
        else:
            ctk.CTkLabel(self.left_content, text="[LOGO]", font=("Arial", 24)).pack(pady=(0, 10))

        # 2. Text Branding
        ctk.CTkLabel(self.left_content, text="FoodShare", 
                     font=("Arial", 36, "bold"), text_color="#E89D30").pack(pady=(0, 15))

        # 3. Slogan
        slogan_frame = ctk.CTkFrame(self.left_content, fg_color="transparent")
        slogan_frame.pack()
        
        ctk.CTkLabel(slogan_frame, text="Share More, ", 
                     font=("Arial", 20, "bold"), text_color="#132A13").pack(side="left")
        ctk.CTkLabel(slogan_frame, text="Waste Less", 
                     font=("Arial", 20, "bold"), text_color="#A4C639").pack(side="left")

        # ===========================================================
        # BAGIAN KANAN: Form Login
        # ===========================================================
        self.right_panel = ctk.CTkFrame(self, fg_color="transparent")
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=(15, 30), pady=30)

        self.form_container = ctk.CTkFrame(self.right_panel, fg_color="transparent", width=350)
        self.form_container.place(relx=0.5, rely=0.5, anchor="center")

        # 1. Header Text
        ctk.CTkLabel(
            self.form_container,
            text="Forgot Password",
            font=("Arial", 28, "bold"),
            text_color=self.colors["text_header"]
        ).pack(pady=(0, 5))

        ctk.CTkLabel(
            self.form_container,
            text="Reset your password here",
            font=("Arial", 14),
            text_color=self.colors["text_sub"]
        ).pack(pady=(0, 40))

        # 2. Input Email
        self.email_entry = ctk.CTkEntry(
            self.form_container,
            width=350,
            height=55,
            corner_radius=15,
            fg_color=self.colors["input_bg"],
            text_color=self.colors["input_fg"],
            placeholder_text="Email",
            placeholder_text_color=self.colors["placeholder"],
            border_width=0,
            font=("Arial", 14)
        )
        self.email_entry.pack(pady=(0, 20))

        # 3. Input Nomor Telepon
        self.phone_entry = ctk.CTkEntry(
            self.form_container,
            width=350,
            height=55,
            corner_radius=15,
            fg_color=self.colors["input_bg"],
            text_color=self.colors["input_fg"],
            placeholder_text="Nomor Telepon",
            placeholder_text_color=self.colors["placeholder"],
            border_width=0,
            font=("Arial", 14)
        )
        self.phone_entry.pack(pady=(0, 20))

        # 4. Input Password Baru
        self.password_entry = ctk.CTkEntry(
            self.form_container,
            width=350,
            height=55,
            corner_radius=15,
            fg_color=self.colors["input_bg"],
            text_color=self.colors["input_fg"],
            placeholder_text="Password Baru",
            placeholder_text_color=self.colors["placeholder"],
            border_width=0,
            show="*",
            font=("Arial", 14)
        )
        self.password_entry.pack(pady=(0, 20))

        # 5. Tombol Reset Password
        self.reset_btn = ctk.CTkButton(
            self.form_container,
            text="Reset Password",
            font=("Arial", 18, "bold"),
            width=350,
            height=55,
            corner_radius=15,
            fg_color=self.colors["btn_bg"],
            text_color="#132A13",
            hover_color=self.colors["btn_hover"],
            cursor="hand2",
            command=self.do_forgot
        )
        self.reset_btn.pack(pady=(10, 25))

        # 6. Kembali ke Login
        back_frame = ctk.CTkFrame(self.form_container, fg_color="transparent")
        back_frame.pack()

        ctk.CTkLabel(
            back_frame, text="Remember your password? ",
            font=("Arial", 12), text_color="#556B2F"
        ).pack(side="left")

        self.back_btn = ctk.CTkButton(
            back_frame,
            text="Login",
            font=("Arial", 12, "bold"),
            fg_color="transparent",
            text_color="#132A13",
            width=50,
            hover_color=self.colors["bg_main"],
            cursor="hand2",
            command=lambda: app.show_frame("LoginPage")
        )
        self.back_btn.bind("<Enter>", lambda e: self.back_btn.configure(text_color="#FFB03B"))
        self.back_btn.bind("<Leave>", lambda e: self.back_btn.configure(text_color="#132A13"))
        self.back_btn.pack(side="left")

    def do_forgot(self):
        email = self.email_entry.get().strip()
        noTelepon = self.phone_entry.get().strip()


        if not email or not noTelepon:
            messagebox.showwarning("Warning", "Mohon lengkapi data login.")
            return
        new_pass = self.password_entry.get().strip()
        data = {
            "email":email,
            "password" : new_pass
        }

        try:
            # result = AkunController.LupaPassword(email, noTelepon,new_pass)
            result = api_forgot_password(email,noTelepon,new_pass)
            if result["status"] == "SUCCESS":
                messagebox.showinfo("Success", "Login berhasil!")
                self.app.login_success(result.user)
            else:
                messagebox.showerror("Error", result["message"])
        except NameError:
            messagebox.showinfo("Test Mode", f"Login UI Checked.\nEmail: {email}\nPass: {new_pass}")