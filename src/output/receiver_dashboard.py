import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import os
from PIL import Image # Tambahan import untuk gambar

from src.output.side_menu import SideMenu
from src.controller.donasi_controller import DonasiController
from src.controller.request_controller import RequestController
from src.model.feedbackdonasi import Feedback

class ReceiverDashboard(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="#F6F6F6")
        self.app = app
        self.current_menu = "Dashboard"
        self.icon_cache = {} # Cache untuk menyimpan icon

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar_frame = None
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        # Load icons saat inisialisasi
        self.load_icons()

    # Fungsi baru: Load Icons (Sama seperti Provider)
    def load_icons(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Pastikan path ini mengarah ke folder assets yang sama
        base_path = os.path.join(script_dir, "../../src/assets") 
        
        # Mapping nama card Receiver ke nama file icon
        icon_names = {
            "Available Foods": "active.png",    # Pakai icon active stock
            "Active Requests": "newrequest.png", # Pakai icon new request
            "Incoming": "delivery.png",         # Pakai icon delivery
            "Total Completed": "completed.png"  # Pakai icon completed
        }
        
        for key, filename in icon_names.items():
            full_path = os.path.join(base_path, filename)
            try:
                pil_image = Image.open(full_path)
                image_size = (24, 24)
                self.icon_cache[key] = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=image_size)
            except FileNotFoundError:
                print(f"ERROR: Icon file not found at {full_path}")
                self.icon_cache[key] = None 

    def show_dashboard(self):
        self.show_dashboard_ui()

    def show_dashboard_ui(self):
        if not getattr(self.app, "current_user", None): return

        if self.sidebar_frame: self.sidebar_frame.destroy()
        self.sidebar_frame = SideMenu(
            self, 
            self.app, 
            menu_items=[
                ("Dashboard", lambda: self.switch_menu("Dashboard")),
                ("Available Food", lambda: self.switch_menu("Available Food")),
                ("My Requests", lambda: self.switch_menu("My Requests")),
                ("Feedback", lambda: self.switch_menu("Feedback")),
            ],
            active_item=self.current_menu
        )
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")

        for widget in self.content_frame.winfo_children(): widget.destroy()

        if self.current_menu == "Dashboard": self.render_overview()
        elif self.current_menu == "Available Food": self.render_available_food()
        elif self.current_menu == "My Requests": self.render_my_requests()
        elif self.current_menu == "Feedback": self.render_feedback()

    def switch_menu(self, menu_name):
        self.current_menu = menu_name
        self.show_dashboard_ui()

    # ============================================
    # 1. OVERVIEW
    # ============================================
    def render_overview(self):
        user = self.app.current_user
        ctk.CTkLabel(self.content_frame, text=f"Hi, {user.nama}!", font=("Arial", 24, "bold"), text_color="#132A13").pack(anchor="w")
        ctk.CTkLabel(self.content_frame, text="Here's your FoodShare summary today.", text_color="gray").pack(anchor="w", pady=(0, 20))

        stats = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        stats.pack(fill="x")

        donasi_aktif = len(DonasiController.getDonasiAktif())
        my_reqs = [r for r in RequestController.semuaRequest() if str(r.idReceiver) == str(user.id)]
        
        # Pastikan title di sini sama dengan Key di self.icon_names
        self.create_stat_card(stats, "Available Foods", str(donasi_aktif)).pack(side="left", expand=True, fill="x", padx=5)
        self.create_stat_card(stats, "Active Requests", str(len(my_reqs))).pack(side="left", expand=True, fill="x", padx=5)
        self.create_stat_card(stats, "Incoming", "0").pack(side="left", expand=True, fill="x", padx=5)
        self.create_stat_card(stats, "Total Completed", "0").pack(side="left", expand=True, fill="x", padx=5)

    def create_stat_card(self, parent, title, value):
        card = ctk.CTkFrame(parent, fg_color="#132A13", corner_radius=10)
        
        # Membuat background lingkaran putih
        icon_bg = ctk.CTkFrame(card, width=40, height=40, corner_radius=20, fg_color="white")
        icon_bg.pack(anchor="w", padx=15, pady=(15, 5))
        
        # Mengambil icon dari cache berdasarkan title card
        ctk_image = self.icon_cache.get(title)
        
        if ctk_image:
            # Menaruh gambar di tengah lingkaran putih
            icon_label = ctk.CTkLabel(icon_bg, text="", image=ctk_image)
            icon_label.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        else:
            # Fallback jika icon tidak ketemu
            ctk.CTkLabel(icon_bg, text="?", text_color="#132A13", font=("Arial", 16, "bold")).place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        ctk.CTkLabel(card, text=title, text_color="#A0B0A0", font=("Arial", 12)).pack(anchor="w", padx=15)
        ctk.CTkLabel(card, text=value, text_color="white", font=("Arial", 28, "bold")).pack(anchor="w", padx=15, pady=(0, 15))
        return card

    # Tambahkan placeholder method render lainnya agar tidak error saat dijalankan
    def render_available_food(self):
        ctk.CTkLabel(self.content_frame, text="Available Food Page").pack()
        
    def render_my_requests(self):
        ctk.CTkLabel(self.content_frame, text="My Requests Page").pack()

    def render_feedback(self):
        ctk.CTkLabel(self.content_frame, text="Feedback Page").pack()

    # ============================================
    # 2. AVAILABLE FOOD (GRID CARD)
    # ============================================
    def render_available_food(self):
        ctk.CTkLabel(self.content_frame, text="Available Food", font=("Arial", 24, "bold"), text_color="#132A13").pack(anchor="w")
        ctk.CTkLabel(self.content_frame, text="Browse and request available donations", text_color="gray").pack(anchor="w", pady=(0, 20))

        scroll = ctk.CTkScrollableFrame(self.content_frame, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        scroll.grid_columnconfigure(0, weight=1)
        scroll.grid_columnconfigure(1, weight=1)
        scroll.grid_columnconfigure(2, weight=1)

        donasi_list = DonasiController.getDonasiAktif()
        
        for i, d in enumerate(donasi_list):
            row = i // 3
            col = i % 3
            self.create_food_card(scroll, d).grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

    def create_food_card(self, parent, donasi):
        # Card background
        card = ctk.CTkFrame(parent, fg_color="#132A13", corner_radius=15)
        
        # Image Placeholder
        img_ph = ctk.CTkFrame(card, height=120, fg_color="#C5E064", corner_radius=10)
        img_ph.pack(fill="x", padx=15, pady=15)
        
        ctk.CTkLabel(card, text=donasi.jenisMakanan, font=("Arial", 16, "bold"), text_color="white", anchor="w").pack(fill="x", padx=15)
        ctk.CTkLabel(card, text=f"Provider #{donasi.idProvider}", font=("Arial", 12), text_color="#A0B0A0", anchor="w").pack(fill="x", padx=15)
        
        detail_text = f"Portions: {donasi.jumlahPorsi}\nExpires: {donasi.batasWaktu}\nLoc: {donasi.lokasi}"
        ctk.CTkLabel(card, text=detail_text, font=("Arial", 12), text_color="white", justify="left", anchor="w").pack(fill="x", padx=15, pady=10)

        # Tombol dengan hover effect
        btn = ctk.CTkButton(card, text="Request Food", fg_color="#F6A836", 
                            hover_color="#E59930", text_color="white", font=("Arial", 14, "bold"),
                            cursor="hand2",
                            command=lambda: self.do_request(donasi.idDonasi))
        btn.pack(fill="x", padx=15, pady=(0, 20))
        
        return card

    def do_request(self, idDonasi):
        if messagebox.askyesno("Confirm", "Request this food?"):
            result = RequestController.buatRequest(idDonasi, self.app.current_user.id)
            if result["status"] == "SUCCESS":
                messagebox.showinfo("Success", "Request sent!")
                self.switch_menu("My Requests")
            else:
                messagebox.showerror("Error", result["message"])

    # ============================================
    # 3. MY REQUESTS (Tabel / List)
    # ============================================
    def render_my_requests(self):
        ctk.CTkLabel(self.content_frame, text="My Requests", font=("Arial", 24, "bold"), text_color="#132A13").pack(anchor="w")
        
        scroll = ctk.CTkScrollableFrame(self.content_frame, fg_color="transparent")
        scroll.pack(fill="both", expand=True, pady=20)

        my_reqs = [r for r in RequestController.semuaRequest() if str(r.idReceiver) == str(self.app.current_user.id)]
        
        for req in my_reqs:
            card = ctk.CTkFrame(scroll, fg_color="#132A13", corner_radius=10)
            card.pack(fill="x", pady=10)
            
            info_frame = ctk.CTkFrame(card, fg_color="transparent")
            info_frame.pack(side="left", padx=20, pady=20)
            
            ctk.CTkLabel(info_frame, text=f"Request #{req.idRequest}", font=("Arial", 16, "bold"), text_color="#C5E064", anchor="w").pack(fill="x")
            ctk.CTkLabel(info_frame, text=f"Donation ID: {req.idDonasi}", text_color="white", anchor="w").pack(fill="x")
            
            status_frame = ctk.CTkFrame(card, fg_color="transparent")
            status_frame.pack(side="right", padx=20)
            
            s_color = "#FEF9C3"
            s_fg = "#A16207"
            if req.status == "Pending": s_text = "Waiting Confirmation"
            else:
                s_text = req.status
                if req.status == "Completed": s_color, s_fg = "#DCFCE7", "#166534"

            ctk.CTkLabel(status_frame, text=s_text, fg_color=s_color, text_color=s_fg, corner_radius=10, width=150, height=30).pack()

    # ============================================
    # 4. FEEDBACK
    # ============================================
    def render_feedback(self):
        ctk.CTkLabel(self.content_frame, text="Feedback History", font=("Arial", 24, "bold"), text_color="#132A13").pack(anchor="w")
        scroll = ctk.CTkScrollableFrame(self.content_frame, fg_color="transparent")
        scroll.pack(fill="both", expand=True, pady=20)

        feedbacks = Feedback.all() 
        for fb in feedbacks:
            card = ctk.CTkFrame(scroll, fg_color="white", border_width=1, border_color="#DDD")
            card.pack(fill="x", pady=10, ipadx=20, ipady=20)
            
            ctk.CTkLabel(card, text=f"To Provider #{fb.idProvider}", font=("Arial", 14, "bold"), text_color="#132A13").pack(anchor="w")
            ctk.CTkLabel(card, text="★"*fb.rating, text_color="#F6A836").pack(anchor="w")
            ctk.CTkLabel(card, text=fb.komentar, text_color="#555").pack(anchor="w", pady=(5, 0))