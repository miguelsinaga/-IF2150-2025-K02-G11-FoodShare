# src/view/admin_dashboard.py
import tkinter as tk
from tkinter import ttk

from src.output.components.side_menu import SideMenu
from src.model.user import Pengguna
from src.model.makanan import DataMakanan
from src.model.reqdonasi import RequestDonasi
from src.model.feedbackdonasi import Feedback


class AdminDashboard(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#E5E7EB")
        self.app = app

        # LEFT MENU
        self.side = SideMenu(
            parent=self,
            app=app,
            menu_items=[
                ("Dashboard", self.show_dashboard),
                ("Daftar User", self.show_users),
                ("Daftar Donasi", self.show_donasi),
                ("Daftar Request", self.show_requests),
                ("Daftar Feedback", self.show_feedback),
            ]
        )
        self.side.pack(side="left", fill="y")

        # RIGHT CONTENT
        self.content = tk.Frame(self, bg="#F9FAFB")
        self.content.pack(side="right", fill="both", expand=True)

        self.show_dashboard()

    # Utility
    def clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    # ------------------------------------
    # DASHBOARD SUMMARY PAGE
    # ------------------------------------
    def show_dashboard(self):
        self.clear_content()

        tk.Label(self.content, text="Dashboard Admin",
                 font=("Helvetica", 26, "bold"),
                 bg="#F9FAFB").pack(pady=25)

        # Fetch data
        total_user = len(Pengguna.all())
        total_donasi = len(DataMakanan.all())
        total_request = len(RequestDonasi.all())
        total_feedback = len(Feedback.all())

        # Stats grid
        grid = tk.Frame(self.content, bg="#F9FAFB")
        grid.pack(pady=20)

        def create_card(parent, title, value):
            card = tk.Frame(parent, bg="white", width=230, height=130, padx=20, pady=20)
            card.pack_propagate(False)
            card.pack(side="left", padx=20)
            tk.Label(card, text=title, font=("Helvetica", 14, "bold"), bg="white").pack()
            tk.Label(card, text=value, font=("Helvetica", 28, "bold"),
                     fg="#2563EB", bg="white").pack()

        create_card(grid, "Total User", total_user)
        create_card(grid, "Total Donasi", total_donasi)
        create_card(grid, "Total Request", total_request)
        create_card(grid, "Total Feedback", total_feedback)

    # ------------------------------------
    # DAFTAR USER
    # ------------------------------------
    def show_users(self):
        self.clear_content()

        tk.Label(self.content, text="Daftar User",
                 font=("Helvetica", 24, "bold"), bg="#F9FAFB").pack(pady=20)

        frame = tk.Frame(self.content, bg="white")
        frame.pack(padx=20, pady=20)

        cols = ("ID", "Nama", "Email", "Role", "Status")
        table = ttk.Treeview(frame, columns=cols, show="headings", height=15)

        for c in cols:
            table.heading(c, text=c)
            table.column(c, width=180)

        table.pack()

        for u in Pengguna.all():
            table.insert("", "end", values=(
                u.id, u.nama, u.email, u.role, u.status
            ))

    # ------------------------------------
    # DAFTAR DONASI
    # ------------------------------------
    def show_donasi(self):
        self.clear_content()

        tk.Label(self.content, text="Daftar Donasi",
                 font=("Helvetica", 24, "bold"), bg="#F9FAFB").pack(pady=20)

        frame = tk.Frame(self.content, bg="white")
        frame.pack(padx=20, pady=20)

        cols = ("ID", "Provider", "Jenis", "Porsi", "Lokasi", "Batas", "Status")
        table = ttk.Treeview(frame, columns=cols, show="headings", height=15)

        for c in cols:
            table.heading(c, text=c)
            table.column(c, width=140)

        table.pack()

        for d in DataMakanan.all():
            table.insert("", "end", values=(
                d.idDonasi, d.idProvider, d.jenisMakanan, d.jumlahPorsi,
                d.lokasi, d.batasWaktu, d.status
            ))

    # ------------------------------------
    # DAFTAR REQUEST
    # ------------------------------------
    def show_requests(self):
        self.clear_content()

        tk.Label(self.content, text="Daftar Request Donasi",
                 font=("Helvetica", 24, "bold"), bg="#F9FAFB").pack(pady=20)

        frame = tk.Frame(self.content, bg="white")
        frame.pack(padx=20, pady=20)

        cols = ("ID Request", "ID Donasi", "Receiver", "Status", "Tanggal")
        table = ttk.Treeview(frame, columns=cols, show="headings", height=15)

        for c in cols:
            table.heading(c, text=c)
            table.column(c, width=160)

        table.pack()

        for r in RequestDonasi.all():
            table.insert("", "end", values=(
                r.idRequest, r.idDonasi, r.idReceiver, r.status, r.tanggalRequest
            ))

    # ------------------------------------
    # DAFTAR FEEDBACK
    # ------------------------------------
    def show_feedback(self):
        self.clear_content()

        tk.Label(self.content, text="Daftar Feedback",
                 font=("Helvetica", 24, "bold"), bg="#F9FAFB").pack(pady=20)

        frame = tk.Frame(self.content, bg="white")
        frame.pack(padx=20, pady=20)

        cols = ("ID", "Provider", "Receiver", "Rating", "Komentar", "Tanggal")
        table = ttk.Treeview(frame, columns=cols, show="headings", height=15)

        for c in cols:
            table.heading(c, text=c)
            table.column(c, width=160)

        table.pack()

        for f in Feedback.all():
            table.insert("", "end", values=(
                f.idFeedback, f.idProvider, f.idReceiver,
                f.rating, f.komentar, f.tanggalFeedback
            ))
