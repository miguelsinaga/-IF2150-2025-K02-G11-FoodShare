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

class LoginPage(ctk.CTkFrame):
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
        # Kartu putih ini tidak menempel penuh ke tepi (ada margin)
        # corner_radius=30 membuat sudutnya melengkung besar seperti di gambar
        self.left_card = ctk.CTkFrame(
            self, 
            fg_color=self.colors["card_bg"], 
            corner_radius=40 
        )
        # padx/pady di sini menciptakan efek "mengambang" dari tepi layar
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
                                           size=(220, 220)) # Ukuran logo diperbesar sedikit
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
        # BAGIAN KANAN: Form Login (Langsung di atas Background Hijau)
        # ===========================================================
        self.right_panel = ctk.CTkFrame(self, fg_color="transparent")
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=(15, 30), pady=30)

        # Container Form
        self.form_container = ctk.CTkFrame(self.right_panel, fg_color="transparent", width=350)
        self.form_container.place(relx=0.5, rely=0.5, anchor="center")

        # 1. Header Text
        ctk.CTkLabel(self.form_container, text="Welcome Back!", 
                     font=("Arial", 28, "bold"), text_color=self.colors["text_header"]).pack(pady=(0, 5))
        
        ctk.CTkLabel(self.form_container, text="Login to your account", 
                     font=("Arial", 14), text_color=self.colors["text_sub"]).pack(pady=(0, 40))

        # 2. Input Email
        self.email_entry = ctk.CTkEntry(
            self.form_container,
            width=350,
            height=55,                       # Lebih tebal sesuai gambar
            corner_radius=15,                # Sudut melengkung
            fg_color=self.colors["input_bg"],
            text_color=self.colors["input_fg"],
            placeholder_text="Email",
            placeholder_text_color=self.colors["placeholder"],
            border_width=0,
            font=("Arial", 14)
        )
        self.email_entry.pack(pady=(0, 20))

        # 3. Input Password
        self.password_entry = ctk.CTkEntry(
            self.form_container,
            width=350,
            height=55,
            corner_radius=15,
            fg_color=self.colors["input_bg"],
            text_color=self.colors["input_fg"],
            placeholder_text="Password",
            placeholder_text_color=self.colors["placeholder"],
            border_width=0,
            show="*",
            font=("Arial", 14)
        )
        self.password_entry.pack(pady=(0, 10))

        # 4. Forgot Password Link
        forgot_btn = ctk.CTkButton(
            self.form_container, 
            text="Forgot Password?", 
            font=("Arial", 12, "bold"),
            fg_color="transparent", 
            text_color="#132A13",
            hover=False,
            anchor="e",
            width=350,
            command=lambda: print("Forgot Password clicked")
        )
        forgot_btn.pack(pady=(0, 25))

        # 5. Tombol Login
        self.login_btn = ctk.CTkButton(
            self.form_container,
            text="Login",
            font=("Arial", 18, "bold"),
            width=350,
            height=55,
            corner_radius=15,
            fg_color=self.colors["btn_bg"],
            text_color="#132A13",
            hover_color=self.colors["btn_hover"],
            command=self.do_login
        )
        self.login_btn.pack(pady=(0, 25))

        # 6. Sign Up Area
        signup_frame = ctk.CTkFrame(self.form_container, fg_color="transparent")
        signup_frame.pack()

        ctk.CTkLabel(signup_frame, text="Don't have an account? ", 
                     font=("Arial", 12), text_color="#556B2F").pack(side="left")
        
        signup_btn = ctk.CTkButton(
            signup_frame,
            text="sign up",
            font=("Arial", 12, "bold"),
            fg_color="transparent",
            text_color="#132A13",
            width=50,
            hover=False,
            command=lambda: app.show_frame("RegisterPage")
        )
        signup_btn.pack(side="left")

    def do_login(self):
        email = self.email_entry.get().strip()
        pw = self.password_entry.get().strip()

        if not email or not pw:
            messagebox.showwarning("Warning", "Mohon lengkapi data login.")
            return

        try:
            result = AkunController.prosesLogin(email, pw)
            if result["status"] == "SUCCESS":
                messagebox.showinfo("Success", "Login berhasil!")
                self.app.login_success(result["user"])
            else:
                messagebox.showerror("Error", result["message"])
        except NameError:
            messagebox.showinfo("Test Mode", f"Login UI Checked.\nEmail: {email}\nPass: {pw}")