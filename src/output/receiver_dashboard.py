# src/view/receiver_dashboard.py
import tkinter as tk
from tkinter import ttk, messagebox

from src.output.components.side_menu import SideMenu
from src.controller.donasi_controller import DonasiController
from src.controller.request_controller import RequestController


class ReceiverDashboard(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#E5E7EB")
        self.app = app
        
        # LEFT MENU
        self.side = SideMenu(
            parent=self,
            app=app,
            menu_items=[
                ("Dashboard", self.show_dashboard),
                ("Donasi Tersedia", self.show_available_donations),
                ("Request Saya", self.show_my_requests),
            ]
        )
        self.side.pack(side="left", fill="y")

        # MAIN CONTENT AREA
        self.content = tk.Frame(self, bg="#F9FAFB")
        self.content.pack(side="right", fill="both", expand=True)

        self.show_dashboard()

    # Utility
    def clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    # --------------------------
    # DASHBOARD SUMMARY
    # --------------------------
    def show_dashboard(self):
        self.clear_content()

        tk.Label(self.content, text="Dashboard Receiver",
                 font=("Helvetica", 24, "bold"),
                 bg="#F9FAFB").pack(pady=20)

        # Count data
        all_requests = RequestController.semuaRequest()
        my_requests = [
            r for r in all_requests 
            if str(r.idReceiver) == str(self.app.current_user.id)
        ]

        card = tk.Frame(self.content, bg="white", padx=30, pady=30)
        card.pack(pady=40)

        tk.Label(card, text="Total Request Anda",
                 font=("Helvetica", 18, "bold"), bg="white").pack()

        tk.Label(card, text=len(my_requests),
                 font=("Helvetica", 28, "bold"), fg="#2563EB", bg="white").pack(pady=10)

    # --------------------------
    #  DONASI TERSEDIA
    # --------------------------
    def show_available_donations(self):
        self.clear_content()

        tk.Label(self.content, text="Donasi Tersedia",
                 font=("Helvetica", 24, "bold"), bg="#F9FAFB").pack(pady=20)

        table_frame = tk.Frame(self.content, bg="white")
        table_frame.pack(pady=20, padx=20)

        cols = ("ID", "Jenis", "Porsi", "Lokasi", "Batas")
        self.table = ttk.Treeview(table_frame, columns=cols, show="headings", height=12)

        for c in cols:
            self.table.heading(c, text=c)
            self.table.column(c, width=150)

        self.table.pack()

        # Load data
        aktif = DonasiController.getDonasiAktif()
        for d in aktif:
            self.table.insert("", "end", values=(
                d.idDonasi, d.jenisMakanan, d.jumlahPorsi, d.lokasi, d.batasWaktu
            ))

        tk.Button(
            self.content,
            text="Request Donasi",
            bg="#10B981", fg="white",
            font=("Helvetica", 12, "bold"),
            command=self.request_selected
        ).pack(pady=10)

    def request_selected(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning("Error", "Pilih donasi terlebih dahulu.")
            return

        row = self.table.item(selected[0])["values"]
        idDonasi = row[0]

        result = RequestController.buatRequest(idDonasi, self.app.current_user.id)

        if result["status"] == "SUCCESS":
            messagebox.showinfo("Sukses", "Request berhasil dibuat!")
            self.show_my_requests()
        else:
            messagebox.showerror("Error", result["message"])

    # --------------------------
    #  REQUEST SAYA
    # --------------------------
    def show_my_requests(self):
        self.clear_content()

        tk.Label(self.content, text="Request Saya",
                 font=("Helvetica", 24, "bold"), bg="#F9FAFB").pack(pady=20)

        table_frame = tk.Frame(self.content, bg="white")
        table_frame.pack(pady=20, padx=20)

        cols = ("ID Request", "ID Donasi", "Status", "Tanggal")
        table = ttk.Treeview(table_frame, columns=cols, show="headings", height=12)

        for c in cols:
            table.heading(c, text=c)
            table.column(c, width=160)

        table.pack()

        all_req = RequestController.semuaRequest()

        for r in all_req:
            if str(r.idReceiver) == str(self.app.current_user.id):
                table.insert("", "end", values=(
                    r.idRequest, r.idDonasi, r.status, r.tanggalRequest
                ))
