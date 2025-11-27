import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import os
import hashlib
import logging
from PIL import Image

from src.frontend.side_menu import SideMenu
from src.controller.donasi_controller import DonasiController
from src.controller.request_controller import RequestController
from src.model.feedbackdonasi import Feedback
from src.controller.feedback_controller import FeedbackController
from src.model.makanan import DataMakanan

class ReceiverDashboard(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="#F6F6F6")
        self.app = app
        self.current_menu = "Dashboard"
        self.icon_cache = {}
        self.my_request_filter = "All"

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar_frame = None
        
        # Main area with header and content separation
        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.grid(row=0, column=1, sticky="nsew")
        
        # Header frame (white background, fixed height)
        self.header_frame = ctk.CTkFrame(self.main_area, height=80, fg_color="#FFFFFF", corner_radius=0)
        self.header_frame.pack(side="top", fill="x")
        self.header_frame.pack_propagate(False)
        
        # Shadow separator
        shadow = ctk.CTkFrame(self.main_area, height=2, fg_color="#E5E7EB", corner_radius=0)
        shadow.pack(side="top", fill="x")
        
        # Content frame
        self.content_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.content_frame.pack(side="top", fill="both", expand=True, padx=20, pady=20)
        
        self.load_icons()

    def load_icons(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.join(script_dir, "../../img") 
        
        icon_names = {
            "Available Foods": "active.png",
            "Active Requests": "newrequest.png",
            "Incoming": "delivery.png",
            "Total Completed": "completed.png"
        }
        
        for key, filename in icon_names.items():
            full_path = os.path.join(base_path, filename)
            try:
                pil_image = Image.open(full_path)
                image_size = (24, 24)
                self.icon_cache[key] = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=image_size)
            except FileNotFoundError:
                print(f"Icon file not found at {full_path}")
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
                ("Profile", lambda: self.switch_menu("Profile")),
            ],
            active_item=self.current_menu
        )
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")

        self.refresh_content()

    def switch_menu(self, menu_name):
        self.current_menu = menu_name
        self.show_dashboard_ui()

    def refresh_content(self):
        # Guard: if account banned, force logout
        try:
            if str(getattr(self.app.current_user, "status", "")).lower() == "banned":
                from tkinter import messagebox
                messagebox.showerror("Akun Diblokir", "Akun Anda diblokir dan tidak dapat menggunakan dashboard.")
                self.app.current_user = None
                self.app.show_frame("LoginPage")
                return
        except Exception:
            pass
        # Clear both header and content
        for widget in self.header_frame.winfo_children(): widget.destroy()
        for widget in self.content_frame.winfo_children(): widget.destroy()

        if self.current_menu == "Dashboard":
            self.render_header("Dashboard", "Here's your FoodShare summary today")
            self.render_overview()
        elif self.current_menu == "Available Food":
            self.render_header("Available Food", "Browse and request available donations")
            self.render_available_food()
        elif self.current_menu == "My Requests":
            self.render_header("My Requests", "Track your food requests")
            self.render_my_requests()
        elif self.current_menu == "Feedback":
            self.render_header("Feedback", "Your feedback history")
            self.render_feedback()
        elif self.current_menu == "Profile":
            self.render_header("Profile", "Manage your profile settings")
            self.render_profile()

    def render_header(self, title, subtitle):
        # Left side - Title and subtitle
        left_container = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        left_container.pack(side="left", padx=30, pady=15)
        
        ctk.CTkLabel(
            left_container, 
            text=title, 
            font=("Arial", 24, "bold"), 
            text_color="#132A13"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            left_container, 
            text=subtitle, 
            font=("Arial", 13), 
            text_color="gray"
        ).pack(anchor="w")

        # Right side - User info with avatar
        right_container = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        right_container.pack(side="right", padx=30)

        user = self.app.current_user
        initials = user.nama[:2].upper() if user.nama else "??"
        
        # Clickable avatar button
        avatar_button = ctk.CTkButton(
            right_container,
            text=initials,
            width=40,
            height=40,
            corner_radius=20,
            fg_color="#132A13",
            hover_color="#1F381F",
            text_color="#C5E064",
            font=("Arial", 14, "bold"),
            command=lambda: self.switch_menu("Profile")
        )
        avatar_button.pack(side="left", padx=10)

        # User info
        info_frame = ctk.CTkFrame(right_container, fg_color="transparent")
        info_frame.pack(side="left")
        
        ctk.CTkLabel(
            info_frame, 
            text=user.nama, 
            font=("Arial", 14, "bold"), 
            text_color="#132A13"
        ).pack(anchor="w", pady=0)
        
        ctk.CTkLabel(
            info_frame, 
            text="Receiver", 
            font=("Arial", 11), 
            text_color="gray"
        ).pack(anchor="w", pady=0)

    def render_overview(self):
        user = self.app.current_user

        stats = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        stats.pack(fill="x")

        donasi_aktif = len(DonasiController.getDonasiAktif())
        my_reqs = [r for r in RequestController.semuaRequest() if str(r.idReceiver) == str(user.id)]
        
        self.create_stat_card(stats, "Available Foods", str(donasi_aktif)).pack(side="left", expand=True, fill="x", padx=5)
        self.create_stat_card(stats, "Active Requests", str(len(my_reqs))).pack(side="left", expand=True, fill="x", padx=5)
        self.create_stat_card(stats, "Incoming", "0").pack(side="left", expand=True, fill="x", padx=5)
        self.create_stat_card(stats, "Total Completed", "0").pack(side="left", expand=True, fill="x", padx=5)

        # Welcome banner
        banner = ctk.CTkFrame(self.content_frame, fg_color="#DCEE85", corner_radius=10)
        banner.pack(fill="x", pady=30, ipady=10)
        ctk.CTkLabel(
            banner, 
            text=f"🍲 Welcome, {user.nama}! Browse available food and make a request today.", 
            text_color="#132A13", 
            font=("Arial", 16, "bold")
        ).pack(anchor="w", padx=20)

    def create_stat_card(self, parent, title, value):
        card = ctk.CTkFrame(parent, fg_color="#132A13", corner_radius=10)
        
        icon_bg = ctk.CTkFrame(card, width=40, height=40, corner_radius=20, fg_color="white")
        icon_bg.pack(anchor="w", padx=15, pady=(15, 5))
        
        ctk_image = self.icon_cache.get(title)
        
        if ctk_image:
            icon_label = ctk.CTkLabel(icon_bg, text="", image=ctk_image)
            icon_label.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        else:
            ctk.CTkLabel(icon_bg, text="?", text_color="#132A13", font=("Arial", 16, "bold")).place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        ctk.CTkLabel(card, text=title, text_color="#A0B0A0", font=("Arial", 12)).pack(anchor="w", padx=15)
        ctk.CTkLabel(card, text=value, text_color="white", font=("Arial", 28, "bold")).pack(anchor="w", padx=15, pady=(0, 15))
        return card

    def render_available_food(self):
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
        card = ctk.CTkFrame(parent, fg_color="#132A13", corner_radius=15)
        
        img_ph = ctk.CTkFrame(card, height=120, fg_color="#C5E064", corner_radius=10)
        img_ph.pack(fill="x", padx=15, pady=15)
        
        ctk.CTkLabel(card, text=donasi.jenisMakanan, font=("Arial", 16, "bold"), text_color="white", anchor="w").pack(fill="x", padx=15)
        try:
            from src.model.user import Pengguna
            p = Pengguna.find_by_id(donasi.idProvider)
            provider_display = p.nama if p else f"Provider #{donasi.idProvider}"
        except Exception:
            provider_display = f"Provider #{donasi.idProvider}"
        ctk.CTkLabel(card, text=provider_display, font=("Arial", 12), text_color="#A0B0A0", anchor="w").pack(fill="x", padx=15)
        
        detail_text = f"Portions: {donasi.jumlahPorsi}\nExpires: {donasi.batasWaktu}\nLoc: {donasi.lokasi}"
        ctk.CTkLabel(card, text=detail_text, font=("Arial", 12), text_color="white", justify="left", anchor="w").pack(fill="x", padx=15, pady=10)

        btn = ctk.CTkButton(card, text="Request Food", fg_color="#F6A836", 
                            hover_color="#E59930", text_color="white", font=("Arial", 14, "bold"),
                            cursor="hand2",
                            command=lambda: self.do_request(donasi.idDonasi))
        btn.pack(fill="x", padx=15, pady=(0, 20))
        
        return card

    def do_request(self, idDonasi):
        if messagebox.askyesno("Confirm", "Request this food?"):
            result = RequestController.buatRequest(idDonasi, self.app.current_user.id)
            if result.get("status") == "SUCCESS":
                messagebox.showinfo("Success", "Request sent!")
                self.switch_menu("My Requests")
            else:
                messagebox.showerror("Error", result.get("message", "Gagal request"))

    def render_my_requests(self):
        filter_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        filter_frame.pack(anchor="w", pady=(0, 10))
        filter_map = {
            "All": "All",
            "Pending": "Pending",
            "Preparing": "Preparing",
            "On Delivery": "On Delivery",
            "Completed": "Completed",
            "Feedback Sent": "FeedbackSent",
        }
        for ui_label, status_value in filter_map.items():
            is_active = (status_value == self.my_request_filter)
            fg = "#132A13" if is_active else "white"
            tc = "white" if is_active else "#132A13"
            hover = "#1F381F" if is_active else "#F0F0F0"
            ctk.CTkButton(filter_frame, text=ui_label, fg_color=fg, text_color=tc, width=110, corner_radius=20, border_width=1, border_color="#DDD", hover_color=hover, cursor="hand2", command=lambda s=status_value: self.set_my_request_filter(s)).pack(side="left", padx=5)

        scroll = ctk.CTkScrollableFrame(self.content_frame, fg_color="transparent")
        scroll.pack(fill="both", expand=True, pady=10)
        info = ctk.CTkFrame(scroll, fg_color="#F9FAFB")
        info.pack(fill="x", padx=10, pady=(0,10))
        ctk.CTkLabel(info, text="Once your request is completed, tap 'Rate / Feedback' to submit your review.", text_color="#6B7280").pack(anchor="w", padx=10, pady=8)
        my_reqs_all = [r for r in RequestController.semuaRequest() if str(r.idReceiver) == str(self.app.current_user.id)]
        if self.my_request_filter != "All":
            my_reqs = [r for r in my_reqs_all if r.status == self.my_request_filter or (self.my_request_filter == "Completed" and r.status == "Completed")]
        else:
            my_reqs = my_reqs_all
        def _to_dt(d):
            from datetime import datetime
            if hasattr(d, "strftime"):
                return d
            try:
                return datetime.fromisoformat(str(d))
            except Exception:
                return datetime.min
        my_reqs = sorted(my_reqs, key=lambda r: _to_dt(r.tanggalRequest), reverse=True)
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
            if req.status == "Pending":
                s_text = "Waiting Confirmation"
            else:
                s_text = req.status
                if req.status in ["Completed", "FeedbackSent"]:
                    s_color, s_fg = "#DCFCE7", "#166534"
            ctk.CTkLabel(status_frame, text=s_text, fg_color=s_color, text_color=s_fg, corner_radius=10, width=150, height=30).pack()

            if s_text == "FeedbackSent":
                ctk.CTkLabel(status_frame, text="Feedback sent", text_color="gray").pack(pady=10)
            elif s_text == "Completed":
                ctk.CTkButton(status_frame, text="Rate / Feedback", fg_color="#F6A836", hover_color="#E59930", text_color="white", cursor="hand2",
                               command=lambda r=req: self.popup_feedback(r)).pack(pady=10)

    def set_my_request_filter(self, s):
        self.my_request_filter = s
        self.refresh_content()

    def render_feedback(self):
        # Update header subtitle agar sesuai dengan gaya Figma
        for widget in self.header_frame.winfo_children(): widget.destroy()
        self.render_header("Feedback", "Reviews and ratings you've given to donors")
        
        scroll = ctk.CTkScrollableFrame(self.content_frame, fg_color="transparent")
        scroll.pack(fill="both", expand=True, pady=(10, 0))
        
        try:
            feedbacks = Feedback.by_receiver(self.app.current_user.id)
        except Exception:
            feedbacks = []
            
        if not feedbacks:
            # Tampilan kosong yang lebih rapi
            empty_frame = ctk.CTkFrame(scroll, fg_color="transparent")
            empty_frame.pack(pady=40, fill="x")
            ctk.CTkLabel(empty_frame, text="You haven't given any feedback yet.", font=("Arial", 16, "bold"), text_color="#374151").pack()
            ctk.CTkLabel(empty_frame, text="Your reviews will appear here once submitted.", font=("Arial", 14), text_color="#6B7280").pack(pady=(5,0))
            return

        for fb in feedbacks:
            # Kartu Feedback Individu (Konsisten dengan gaya Provider)
            card = ctk.CTkFrame(scroll, fg_color="white", corner_radius=16, border_width=2, border_color="#E5E7EB")
            card.pack(fill="x", pady=10, ipadx=20, ipady=20)

            # Header Kartu (Nama Provider & Bintang)
            header_row = ctk.CTkFrame(card, fg_color="transparent")
            header_row.pack(fill="x", pady=(0, 10))

            # Nama Provider (Bold)
            # Catatan: Menggunakan ID karena nama asli provider tidak tersedia langsung di objek feedback.
            try:
                from src.model.user import Pengguna
                p = Pengguna.find_by_id(fb.idProvider)
                provider_display = p.nama if p else f"Provider #{fb.idProvider}"
            except Exception:
                provider_display = f"Provider #{fb.idProvider}"
            ctk.CTkLabel(header_row, text=f"To {provider_display}", font=("Arial", 16, "bold"), text_color="#111827").pack(side="left", anchor="w")

            # Rating Bintang Individu (Kanan Atas)
            fb_rating = int(fb.rating)
            ind_stars_full = "★" * fb_rating
            ind_stars_empty = "☆" * (3 - fb_rating)

            star_container = ctk.CTkFrame(header_row, fg_color="transparent")
            star_container.pack(side="right")
            ctk.CTkLabel(star_container, text=ind_stars_full, font=("Arial", 18), text_color="#F6A836").pack(side="left")
            if ind_stars_empty:
                 ctk.CTkLabel(star_container, text=ind_stars_empty, font=("Arial", 18), text_color="#D1D5DB").pack(side="left")

            # Isi Komentar
            comment_text = fb.komentar if fb.komentar else ""
            if comment_text:
                 ctk.CTkLabel(card, text=comment_text, font=("Arial", 14), text_color="#374151", anchor="w", justify="left", wraplength=800).pack(fill="x")
            else:
                 ctk.CTkLabel(card, text="No written review provided.", font=("Arial", 14, "italic"), text_color="#9CA3AF", anchor="w").pack(fill="x")

    def popup_feedback(self, req):
        FeedbackPopup(self.app.master, req, self.app.current_user.id)

class FeedbackPopup(ctk.CTkToplevel):
    def __init__(self, parent, request_obj, receiver_id):
        super().__init__(parent)
        self.request_obj = request_obj
        self.receiver_id = receiver_id
        self.title("Give Feedback")
        self.geometry("400x400")
        donasi = DataMakanan.find_by_id(request_obj.idDonasi)
        self.provider_id = donasi.idProvider if donasi else 0
        ctk.CTkLabel(self, text="Rate your experience", font=("Arial", 18, "bold")).pack(pady=20)

        stars_frame = ctk.CTkFrame(self, fg_color="transparent")
        stars_frame.pack(pady=10)
        self.rating = 3
        self.star_buttons = []
        def set_rating(n):
            self.rating = n
            for i, btn in enumerate(self.star_buttons, start=1):
                filled = i <= n
                btn.configure(text="★" if filled else "☆", text_color="#F6A836" if filled else "#9CA3AF")
            self.lbl_val.configure(text=f"{n} Stars (1–3)")
        for i in range(1,4):
            b = ctk.CTkButton(stars_frame, width=28, height=28, fg_color="white", border_width=1, border_color="#DDD",
                               text="★" if i<=3 else "☆", text_color="#F6A836", command=lambda n=i: set_rating(n))
            b.pack(side="left", padx=3)
            self.star_buttons.append(b)
        self.lbl_val = ctk.CTkLabel(self, text="3 Stars (1–3)")
        self.lbl_val.pack()

        self.placeholder_text = "Write your comment (optional)..."
        self.txt_comment = ctk.CTkTextbox(self, height=100, width=300)
        self.txt_comment.pack(pady=10)
        self.txt_comment.insert("1.0", self.placeholder_text)
        self.placeholder_active = True
        def on_focus_in(event):
            if self.placeholder_active:
                self.txt_comment.delete("1.0", "end")
                self.placeholder_active = False
        def on_focus_out(event):
            content = self.txt_comment.get("1.0", "end").strip()
            if not content:
                self.txt_comment.delete("1.0", "end")
                self.txt_comment.insert("1.0", self.placeholder_text)
                self.placeholder_active = True
        self.txt_comment.bind("<FocusIn>", on_focus_in)
        self.txt_comment.bind("<FocusOut>", on_focus_out)

        ctk.CTkButton(self, text="Submit", fg_color="#132A13", command=self.submit).pack(pady=10)

    def submit(self):
        logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        rating = int(self.rating)
        if rating not in {1,2,3}:
            messagebox.showerror("Error", "Rating harus 1, 2, atau 3")
            return
        comment = self.txt_comment.get("1.0", "end").strip()
        if self.placeholder_active or comment == self.placeholder_text:
            comment = ""
        # Duplicate check dihapus: feedback diperbolehkan per request.
        logger.info("feedback_submit_start receiver_id=%s provider_id=%s request_id=%s rating=%s", self.receiver_id, self.provider_id, self.request_obj.idRequest, rating)
        res = FeedbackController.kirimFeedback(self.provider_id, self.receiver_id, rating, comment)
        if res.get("status") == "SUCCESS":
            from src.controller.request_controller import RequestController
            upd = RequestController.updateStatus(self.request_obj.idRequest, "FeedbackSent")
            if upd.get("status") == "SUCCESS":
                logger.info("feedback_submit_success receiver_id=%s provider_id=%s request_id=%s status=FeedbackSent", self.receiver_id, self.provider_id, self.request_obj.idRequest)
                messagebox.showinfo("Sukses", "Feedback berhasil dikirim!")
            else:
                logger.error("feedback_status_update_failed receiver_id=%s provider_id=%s request_id=%s error=%s", self.receiver_id, self.provider_id, self.request_obj.idRequest, upd.get("message"))
                messagebox.showwarning("Tersimpan", "Feedback tersimpan, namun gagal mengubah status request.")
            self.destroy()
        else:
            logger.error("feedback_submit_failed receiver_id=%s provider_id=%s request_id=%s error=%s", self.receiver_id, self.provider_id, self.request_obj.idRequest, res.get("message"))
            messagebox.showerror("Error", res.get("message", "Gagal mengirim feedback"))

    def do_request(self, idDonasi):
        if messagebox.askyesno("Confirm", "Request this food?"):
            result = RequestController.buatRequest(idDonasi, self.app.current_user.id)
            if result.get("status") == "SUCCESS":
                messagebox.showinfo("Success", "Request sent!")
                self.switch_menu("My Requests")
            else:
                messagebox.showerror("Error", result.get("message", "Gagal request"))
