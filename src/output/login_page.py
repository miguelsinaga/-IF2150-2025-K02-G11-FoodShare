# src/view/login_page.py
import tkinter as tk
from tkinter import messagebox
from src.controller.account_controller import AkunController

class LoginPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#F5F5F5")
        self.app = app

        tk.Label(self, text="Selamat Datang",
                 font=("Helvetica", 28, "bold"),
                 bg="#F5F5F5").pack(pady=40)

        tk.Label(self, text="Silakan login untuk melanjutkan",
                 font=("Helvetica", 14),
                 bg="#F5F5F5").pack()

        # Card
        card = tk.Frame(self, bg="white", padx=30, pady=30)
        card.pack(pady=40)

        # Email
        tk.Label(card, text="Email", font=("Helvetica", 12), bg="white").grid(row=0, column=0, sticky="w")
        self.email_entry = tk.Entry(card, width=35)
        self.email_entry.grid(row=1, column=0, pady=8)

        # Password
        tk.Label(card, text="Password", font=("Helvetica", 12), bg="white").grid(row=2, column=0, sticky="w")
        self.password_entry = tk.Entry(card, width=35, show="*")
        self.password_entry.grid(row=3, column=0, pady=8)

        # Button
        tk.Button(card, text="Login", width=20,
                  bg="#007BFF", fg="white",
                  command=self.do_login).grid(row=4, column=0, pady=15)

        tk.Button(self, text="Belum punya akun? Register",
                  bg="#F5F5F5", fg="blue", relief="flat",
                  command=lambda: app.show_frame("RegisterPage")).pack()

    def do_login(self):
        email = self.email_entry.get().strip()
        pw = self.password_entry.get().strip()

        result = AkunController.prosesLogin(email, pw)

        if result["status"] == "SUCCESS":
            messagebox.showinfo("Success", "Login berhasil!")
            self.app.login_success(result["user"])
        else:
            messagebox.showerror("Error", result["message"])
