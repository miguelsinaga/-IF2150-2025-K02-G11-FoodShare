# src/view/register_page.py
import tkinter as tk
from tkinter import ttk, messagebox
from src.controller.account_controller import AkunController

class RegisterPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#F5F5F5")
        self.app = app

        tk.Label(self, text="Buat Akun Baru",
                 font=("Helvetica", 26, "bold"),
                 bg="#F5F5F5").pack(pady=30)

        card = tk.Frame(self, bg="white", padx=30, pady=30)
        card.pack(pady=20)

        # Nama
        tk.Label(card, text="Nama Lengkap", bg="white").grid(row=0, column=0, sticky="w")
        self.nama = tk.Entry(card, width=35)
        self.nama.grid(row=1, column=0, pady=8)

        # Email
        tk.Label(card, text="Email", bg="white").grid(row=2, column=0, sticky="w")
        self.email = tk.Entry(card, width=35)
        self.email.grid(row=3, column=0, pady=8)

        # Password
        tk.Label(card, text="Password", bg="white").grid(row=4, column=0, sticky="w")
        self.password = tk.Entry(card, width=35, show="*")
        self.password.grid(row=5, column=0, pady=8)

        # Telepon
        tk.Label(card, text="No Telepon", bg="white").grid(row=6, column=0, sticky="w")
        self.notelp = tk.Entry(card, width=35)
        self.notelp.grid(row=7, column=0, pady=8)

        # Role
        tk.Label(card, text="Daftar sebagai", bg="white").grid(row=8, column=0, sticky="w")
        self.role = ttk.Combobox(card, values=["provider", "receiver"], width=32)
        self.role.grid(row=9, column=0, pady=8)
        self.role.current(0)

        tk.Button(card, text="Daftar", bg="#28A745", fg="white", width=20,
                  command=self.do_register).grid(row=10, column=0, pady=20)

        tk.Button(self, text="Sudah punya akun? Login",
                  fg="blue", bg="#F5F5F5", relief="flat",
                  command=lambda: app.show_frame("LoginPage")).pack()

    def do_register(self):
        data = {
            "nama": self.nama.get().strip(),
            "email": self.email.get().strip(),
            "password": self.password.get().strip(),
            "noTelepon": self.notelp.get().strip(),
            "role": self.role.get().strip()
        }

        result = AkunController.prosesRegistrasi(data)

        if result["status"] == "SUCCESS":
            messagebox.showinfo("Success", "Registrasi berhasil!")
            self.app.show_frame("LoginPage")
        else:
            messagebox.showerror("Error", result["message"])
