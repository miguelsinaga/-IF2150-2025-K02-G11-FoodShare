import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from datetime import datetime

from src.output.side_menu import SideMenu
from src.controller.donasi_controller import DonasiController
from src.controller.request_controller import RequestController
from src.controller.feedback_controller import FeedbackController
from src.model.feedbackdonasi import Feedback

class ProviderDashboard(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="#F6F6F6")
        self.app = app
        self.current_menu = "Dashboard"

        # Layout utama: Grid 2 kolom (Sidebar, Content)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar Container (akan direfresh saat menu berubah)
        self.sidebar_frame = None
        
        # Content Container
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    def show_dashboard_ui(self):
        # Pastikan user login
        if not getattr(self.app, "current_user", None): return

        # Refresh Sidebar dengan active state yang benar
        if self.sidebar_frame: self.sidebar_frame.destroy()
        self.sidebar_frame = SideMenu(
            self, 
            self.app, 
            menu_items=[
                ("Dashboard", lambda: self.switch_menu("Dashboard")),
                ("Food Stock", lambda: self.switch_menu("Food Stock")),
                ("Food Requests", lambda: self.switch_menu("Food Requests")),
                ("Feedback", lambda: self.switch_menu("Feedback")),
                ("Profile", lambda: self.switch_menu("Profile")),
            ],
            active_item=self.current_menu
        )
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")

        # Bersihkan konten lama
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Render konten sesuai menu yang dipilih
        if self.current_menu == "Dashboard":
            self.render_overview()
        elif self.current_menu == "Food Stock":
            self.render_food_stock()
        elif self.current_menu == "Food Requests":
            self.render_food_requests()
        elif self.current_menu == "Feedback":
            self.render_feedback()
        elif self.current_menu == "Profile":
            self.render_profile()

    def switch_menu(self, menu_name):
        self.current_menu = menu_name
        self.show_dashboard_ui()

    # Agar method ini dipanggil oleh MainApp saat frame ditampilkan
    def show_dashboard(self):
        self.show_dashboard_ui()

    # ==============================================================
    # 1. DASHBOARD OVERVIEW
    # ==============================================================
    def render_overview(self):
        user = self.app.current_user
        
        # Header
        ctk.CTkLabel(self.content_frame, text=f"Hi, {user.nama}!", 
                     font=("Arial", 24, "bold"), text_color="#132A13").pack(anchor="w")
        ctk.CTkLabel(self.content_frame, text="Here's an overview of your FoodShare activities today.", 
                     font=("Arial", 14), text_color="gray").pack(anchor="w", pady=(0, 20))

        # Data Stats
        all_donasi = DonasiController.getDonasiAktif()
        my_donasi = [d for d in all_donasi if str(d.idProvider) == str(user.id)]
        
        all_reqs = RequestController.semuaRequest()
        # Filter request untuk donasi milik provider ini
        my_reqs_incoming = []
        completed_count = 0
        for req in all_reqs:
            # Cari donasi terkait request ini
            # (Di real app idealnya join database, di sini manual loop)
            for donasi in all_donasi: # Note: all_donasi might filter 'Tersedia' only in controller, better fetch all
                pass # Logic sederhana: kita butuh hitung status

        # Kartu Statistik
        stats_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        stats_frame.pack(fill="x", pady=10)

        self.create_stat_card(stats_frame, "Active Stocks", str(len(my_donasi)), "#132A13").pack(side="left", expand=True, fill="x", padx=5)
        self.create_stat_card(stats_frame, "New Requests", "0", "#132A13").pack(side="left", expand=True, fill="x", padx=5)
        self.create_stat_card(stats_frame, "On Delivery", "0", "#132A13").pack(side="left", expand=True, fill="x", padx=5)
        self.create_stat_card(stats_frame, "Total Donations", "0", "#132A13").pack(side="left", expand=True, fill="x", padx=5)

        # Banner Hijau Bawah
        banner = ctk.CTkFrame(self.content_frame, fg_color="#DCEE85", corner_radius=10)
        banner.pack(fill="x", pady=30, ipady=10)
        ctk.CTkLabel(banner, text="♻ You've helped share meals this month.", 
                     text_color="#132A13", font=("Arial", 16, "bold")).pack(anchor="w", padx=20)

    def create_stat_card(self, parent, title, value, bg_color):
        card = ctk.CTkFrame(parent, fg_color=bg_color, corner_radius=10)
        
        # Icon placeholder (lingkaran putih)
        icon_bg = ctk.CTkFrame(card, width=40, height=40, corner_radius=20, fg_color="white")
        icon_bg.pack(anchor="w", padx=15, pady=(15, 5))
        
        ctk.CTkLabel(card, text=title, font=("Arial", 12), text_color="#A0B0A0").pack(anchor="w", padx=15)
        ctk.CTkLabel(card, text=value, font=("Arial", 28, "bold"), text_color="white").pack(anchor="w", padx=15, pady=(0, 15))
        return card

    # ==============================================================
    # 2. FOOD STOCK (Availability)
    # ==============================================================
    def render_food_stock(self):
        # Header
        header_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(header_frame, text="Available Food Items", font=("Arial", 20, "bold"), text_color="#132A13").pack(side="left")
        
        ctk.CTkButton(header_frame, text="+ Add Availability", font=("Arial", 13, "bold"),
                      fg_color="#F6A836", hover_color="#E59930", text_color="white",
                      command=self.popup_add_donasi).pack(side="right")

        # Table Container
        table_frame = ctk.CTkScrollableFrame(self.content_frame, fg_color="white", corner_radius=10)
        table_frame.pack(fill="both", expand=True)

        # Table Header
        headers = ["Food Item", "Expiration", "Portions", "Status", "Action"]
        self.create_table_header(table_frame, headers)

        # Table Rows
        donasi_list = DonasiController.getDonasiAktif()
        my_donasi = [d for d in donasi_list if str(d.idProvider) == str(self.app.current_user.id)]

        for item in my_donasi:
            self.create_stock_row(table_frame, item)

    def create_stock_row(self, parent, item):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=10)

        ctk.CTkLabel(row, text=item.jenisMakanan, font=("Arial", 13), width=150, anchor="w", text_color="#333").pack(side="left", padx=10)
        ctk.CTkLabel(row, text=item.batasWaktu, font=("Arial", 13), width=120, anchor="w", text_color="#333").pack(side="left", padx=10)
        ctk.CTkLabel(row, text=str(item.jumlahPorsi), font=("Arial", 13), width=100, anchor="w", text_color="#333").pack(side="left", padx=10)
        
        # Status Badge
        status_color = "#E6F4EA" if item.status == "Tersedia" else "#FCE8E6"
        status_text_color = "#1E8E3E" if item.status == "Tersedia" else "#D93025"
        status_lbl = ctk.CTkLabel(row, text="Active" if item.status=="Tersedia" else item.status, 
                                  fg_color=status_color, text_color=status_text_color, corner_radius=15, width=80)
        status_lbl.pack(side="left", padx=10)

        # Actions
        btn_edit = ctk.CTkButton(row, text="Edit", width=60, fg_color="white", border_width=1, border_color="#DDD", text_color="#333", hover_color="#F0F0F0")
        btn_edit.pack(side="left", padx=5)
        
        btn_del = ctk.CTkButton(row, text="Remove", width=70, fg_color="white", border_width=1, border_color="#EF4444", text_color="#EF4444", hover_color="#FEF2F2",
                                command=lambda: self.hapus_donasi(item.idDonasi))
        btn_del.pack(side="left", padx=5)
        
        # Separator line
        ctk.CTkFrame(parent, height=1, fg_color="#EEE").pack(fill="x")

    # ==============================================================
    # 3. FOOD REQUESTS
    # ==============================================================
    def render_food_requests(self):
        ctk.CTkLabel(self.content_frame, text="All Requests", font=("Arial", 20, "bold"), text_color="#132A13").pack(anchor="w", pady=(0, 20))

        # Filters
        filter_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        filter_frame.pack(anchor="w", pady=(0, 20))
        for f in ["All", "Requested", "Preparing", "On Delivery", "Completed"]:
            fg = "#132A13" if f == "All" else "white"
            tc = "white" if f == "All" else "#333"
            ctk.CTkButton(filter_frame, text=f, fg_color=fg, text_color=tc, width=80, corner_radius=20, border_width=1, border_color="#DDD").pack(side="left", padx=5)

        table_frame = ctk.CTkScrollableFrame(self.content_frame, fg_color="white", corner_radius=10)
        table_frame.pack(fill="both", expand=True)

        headers = ["Req ID", "Food Item", "Receiver", "Date", "Status", "Action"]
        self.create_table_header(table_frame, headers)

        # Data dummy / logic (karena tidak ada relasi langsung user->nama di CSV requests sederhana)
        # Di sini kita fetch semua request, lalu filter yang terkait donasi provider ini
        all_requests = RequestController.semuaRequest()
        # Note: Di sistem nyata, kita perlu join DataMakanan untuk cek providernya
        # Karena keterbatasan model sederhana, saya akan tampilkan semua untuk demo, atau filter by idDonasi
        
        for req in all_requests:
            self.create_request_row(table_frame, req)

    def create_request_row(self, parent, req):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=10)

        ctk.CTkLabel(row, text=f"REQ{req.idRequest}", width=60, anchor="w", text_color="#333").pack(side="left", padx=10)
        ctk.CTkLabel(row, text=f"Donasi #{req.idDonasi}", width=150, anchor="w", text_color="#333").pack(side="left", padx=10) # Nama makanan harusnya di-fetch
        ctk.CTkLabel(row, text=f"User #{req.idReceiver}", width=120, anchor="w", text_color="#333").pack(side="left", padx=10) # Nama receiver harusnya di-fetch
        ctk.CTkLabel(row, text=req.tanggalRequest[:10], width=100, anchor="w", text_color="#333").pack(side="left", padx=10)

        # Status Pill
        s_color = "#FEF9C3" # yellow default
        s_text = "#A16207"
        if req.status == "On Delivery": s_color, s_text = "#DBEAFE", "#1E40AF"
        elif req.status == "Completed": s_color, s_text = "#DCFCE7", "#166534"
        
        ctk.CTkLabel(row, text=req.status, fg_color=s_color, text_color=s_text, corner_radius=15, width=90).pack(side="left", padx=10)

        # Action Buttons
        if req.status == "Pending":
            ctk.CTkButton(row, text="Accept", width=60, fg_color="#10B981", text_color="white").pack(side="left", padx=2)
            ctk.CTkButton(row, text="Reject", width=60, fg_color="white", border_width=1, border_color="red", text_color="red").pack(side="left", padx=2)
        else:
            ctk.CTkButton(row, text="Update", width=80, fg_color="#132A13", text_color="white").pack(side="left", padx=2)

        ctk.CTkFrame(parent, height=1, fg_color="#EEE").pack(fill="x")

    # ==============================================================
    # 4. FEEDBACK
    # ==============================================================
    def render_feedback(self):
        ctk.CTkLabel(self.content_frame, text="Feedback", font=("Arial", 20, "bold"), text_color="#132A13").pack(anchor="w")
        ctk.CTkLabel(self.content_frame, text="See what receivers think about your donations", text_color="gray").pack(anchor="w", pady=(0, 20))

        # Rating Summary
        summary = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=10, border_width=1, border_color="#DDD")
        summary.pack(fill="x", pady=(0, 20), ipadx=20, ipady=20)
        
        ctk.CTkLabel(summary, text="3.7", font=("Arial", 40, "bold"), text_color="#F6A836").pack(side="left", padx=20)
        star_frame = ctk.CTkFrame(summary, fg_color="transparent")
        star_frame.pack(side="left")
        ctk.CTkLabel(star_frame, text="★ ★ ★ ★ ☆", font=("Arial", 20), text_color="#F6A836").pack(anchor="w")
        ctk.CTkLabel(star_frame, text="Based on feedbacks", text_color="gray").pack(anchor="w")

        # List Reviews
        scroll = ctk.CTkScrollableFrame(self.content_frame, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        feedbacks = Feedback.by_provider(self.app.current_user.id)
        for fb in feedbacks:
            card = ctk.CTkFrame(scroll, fg_color="white", corner_radius=10, border_width=1, border_color="#DDD")
            card.pack(fill="x", pady=10, ipadx=15, ipady=15)
            
            # Header card
            h = ctk.CTkFrame(card, fg_color="transparent")
            h.pack(fill="x")
            ctk.CTkLabel(h, text=f"Receiver #{fb.idReceiver}", font=("Arial", 14, "bold"), text_color="#333").pack(side="left")
            ctk.CTkLabel(h, text="★"*fb.rating, text_color="#F6A836").pack(side="right")
            
            ctk.CTkLabel(card, text=fb.komentar, font=("Arial", 14), text_color="#555", anchor="w", justify="left").pack(fill="x", pady=(10, 0))

    # ==============================================================
    # 5. PROFILE
    # ==============================================================
    def render_profile(self):
        ctk.CTkLabel(self.content_frame, text="Profile", font=("Arial", 24, "bold"), text_color="#132A13").pack(anchor="w", pady=(0, 20))
        
        user = self.app.current_user
        form = ctk.CTkScrollableFrame(self.content_frame, fg_color="white", corner_radius=10)
        form.pack(fill="both", expand=True, ipadx=30, ipady=30)

        self.create_profile_field(form, "Name", user.nama)
        self.create_profile_field(form, "Email", user.email)
        self.create_profile_field(form, "Contact Number", user.noTelepon)
        
        ctk.CTkLabel(form, text="Change Password", font=("Arial", 14, "bold"), text_color="#333").pack(anchor="w", pady=(20, 10))
        ctk.CTkEntry(form, placeholder_text="Current Password", width=400).pack(anchor="w", pady=5)
        ctk.CTkEntry(form, placeholder_text="New Password", width=400).pack(anchor="w", pady=5)
        
        btn_frame = ctk.CTkFrame(form, fg_color="transparent")
        btn_frame.pack(fill="x", pady=30)
        
        ctk.CTkButton(btn_frame, text="Save", fg_color="#132A13", text_color="white", width=100).pack(side="right")
        ctk.CTkButton(btn_frame, text="Cancel", fg_color="white", border_width=1, border_color="#333", text_color="#333", width=100).pack(side="right", padx=10)

    def create_profile_field(self, parent, label, value):
        ctk.CTkLabel(parent, text=label, font=("Arial", 12, "bold"), text_color="#333").pack(anchor="w", pady=(10, 5))
        entry = ctk.CTkEntry(parent, width=400)
        entry.insert(0, value)
        entry.pack(anchor="w")

    # --- Helpers ---
    def create_table_header(self, parent, headers):
        header_frame = ctk.CTkFrame(parent, fg_color="#F9FAFB", height=40)
        header_frame.pack(fill="x")
        widths = [150, 120, 100, 100, 150]
        if len(headers) == 6: widths = [60, 150, 120, 100, 100, 100] # Adjustment for requests
        
        for i, h in enumerate(headers):
            w = widths[i] if i < len(widths) else 100
            ctk.CTkLabel(header_frame, text=h, font=("Arial", 12, "bold"), width=w, anchor="w", text_color="#666").pack(side="left", padx=10)
        
        ctk.CTkFrame(parent, height=1, fg_color="#DDD").pack(fill="x")

    def popup_add_donasi(self):
        # Simple placeholder for popup
        messagebox.showinfo("Info", "Fitur Tambah Donasi (Pop-up) akan muncul di sini.\nImplementasi logic sama dengan sebelumnya.")

    def hapus_donasi(self, idDonasi):
        if messagebox.askyesno("Confirm", "Delete this item?"):
            DonasiController.batalkanDonasi(idDonasi)
            self.show_dashboard_ui() # Refresh