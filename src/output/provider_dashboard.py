# src/view/provider_dashboard.py
import tkinter as tk
from tkinter import messagebox, ttk

from src.output.components.side_menu import SideMenu
from src.controller.donasi_controller import DonasiController


class ProviderDashboard(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#E5E7EB")
        self.app = app
        
        # ======= LEFT MENU ========
        self.side = SideMenu(
            parent=self,
            app=app,
            menu_items=[
                ("Dashboard", self.show_dashboard),
                ("Buat Donasi", self.show_create_donation),
                ("Daftar Donasi", self.show_list_donation)
            ]
        )
        self.side.pack(side="left", fill="y")

        # ======= RIGHT CONTENT ========
        self.content = tk.Frame(self, bg="#F9FAFB")
        self.content.pack(side="right", fill="both", expand=True)

        # Do not call `show_dashboard` here — pages are constructed before
        # login and `self.app.current_user` may be None. The frame will be
        # refreshed by `MainApp.show_frame` when it becomes visible.

    # --------------------------
    #   Page Switcher
    # --------------------------
    def clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    # --------------------------
    #   DASHBOARD PAGE
    # --------------------------
    def show_dashboard(self):
        # If no user is logged in yet, show a placeholder.
        if not getattr(self.app, "current_user", None):
            self.clear_content()
            tk.Label(self.content, text="Silakan login untuk melihat dashboard",
                     font=("Helvetica", 16), bg="#F9FAFB").pack(pady=40)
            return

        self.clear_content()

        tk.Label(self.content, text="Dashboard Provider",
                 font=("Helvetica", 24, "bold"),
                 bg="#F9FAFB").pack(pady=20)

        # fetch data
        all_donasi = DonasiController.getDonasiAktif()
        donasi_saya = [
            d for d in all_donasi
            if str(d.idProvider) == str(self.app.current_user.id)
        ]

        card = tk.Frame(self.content, bg="white", padx=20, pady=20)
        card.pack(pady=40)

        tk.Label(card, text="Total Donasi Aktif Anda",
                 font=("Helvetica", 18, "bold"),
                 bg="white").pack(pady=10)

        tk.Label(card, text=str(len(donasi_saya)),
                 font=("Helvetica", 28, "bold"),
                 fg="#2563EB",
                 bg="white").pack(pady=10)

    # --------------------------
    #   CREATE DONATION PAGE
    # --------------------------
    def show_create_donation(self):
        self.clear_content()

        tk.Label(self.content, text="Buat Donasi Baru",
                 font=("Helvetica", 24, "bold"),
                 bg="#F9FAFB").pack(pady=20)

        form = tk.Frame(self.content, bg="white", padx=30, pady=30)
        form.pack(pady=20)

        # Fields
        labels = ["Jenis Makanan", "Jumlah Porsi", "Lokasi", "Batas Waktu (YYYY-MM-DD)"]
        self.inputs = {}

        for i, label in enumerate(labels):
            tk.Label(form, text=label, bg="white", font=("Helvetica", 12)).grid(row=i, column=0, sticky="w")
            entry = tk.Entry(form, width=40)
            entry.grid(row=i, column=1, pady=8)
            self.inputs[label] = entry

        tk.Button(form, text="Submit Donasi",
                  bg="#10B981", fg="white",
                  font=("Helvetica", 12, "bold"), width=20,
                  command=self.submit_donation).grid(row=5, column=0, columnspan=2, pady=20)

    def submit_donation(self):
        data = {
            "jenisMakanan": self.inputs["Jenis Makanan"].get(),
            "jumlahPorsi": self.inputs["Jumlah Porsi"].get(),
            "lokasi": self.inputs["Lokasi"].get(),
            "batasWaktu": self.inputs["Batas Waktu (YYYY-MM-DD)"].get(),
        }

        if not getattr(self.app, "current_user", None):
            messagebox.showerror("Error", "Anda harus login sebagai provider terlebih dahulu.")
            return

        result = DonasiController.buatDonasi(self.app.current_user.id, data)

        if result["status"] == "SUCCESS":
            messagebox.showinfo("Sukses", "Donasi berhasil dibuat!")
            self.show_list_donation()
        else:
            messagebox.showerror("Error", result["message"])

    # --------------------------
    #   DONATION LIST PAGE
    # --------------------------
    def show_list_donation(self):
        self.clear_content()

        tk.Label(self.content, text="Daftar Donasi Anda",
                 font=("Helvetica", 24, "bold"),
                 bg="#F9FAFB").pack(pady=20)

        table_frame = tk.Frame(self.content, bg="white")
        table_frame.pack(pady=20, padx=20)

        cols = ("ID", "Jenis", "Porsi", "Lokasi", "Batas", "Status")
        self.table = ttk.Treeview(table_frame, columns=cols, show="headings", height=12)

        for c in cols:
            self.table.heading(c, text=c)
            self.table.column(c, width=150)

        self.table.pack()

        # If no user is logged in, show placeholder
        if not getattr(self.app, "current_user", None):
            tk.Label(self.content, text="Silakan login untuk melihat daftar donasi",
                     font=("Helvetica", 14), bg="#F9FAFB").pack(pady=20)
            return

        # Load provider's data
        all_donasi = DonasiController.getDonasiAktif()
        donasi_saya = [
            d for d in all_donasi
            if str(d.idProvider) == str(self.app.current_user.id)
        ]

        for d in donasi_saya:
            self.table.insert("", "end", values=(
                d.idDonasi, d.jenisMakanan, d.jumlahPorsi,
                d.lokasi, d.batasWaktu, d.status
            ))
