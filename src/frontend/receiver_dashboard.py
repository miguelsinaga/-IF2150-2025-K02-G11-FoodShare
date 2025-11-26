import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import os
import hashlib
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
        ctk.CTkLabel(card, text=f"Provider #{donasi.idProvider}", font=("Arial", 12), text_color="#A0B0A0", anchor="w").pack(fill="x", padx=15)
        
        detail_text = f"Portions: {donasi.jumlahPorsi}\nExpires: {donasi.batasWaktu}\nLoc: {donasi.lokasi}"
        ctk.CTkLabel(card, text=detail_text, font=("Arial", 12), text_color="white", justify="left", anchor="w").pack(fill="x", padx=15, pady=10)

        btn = ctk.CTkButton(card, text="Request Food", fg_color="#F6A836", 
                            hover_color="#E59930", text_color="white", font=("Arial", 14, "bold"),
                            cursor="hand2",
                            command=lambda: self.do_request(donasi.idDonasi))
        btn.pack(fill="x", padx=15, pady=(0, 20))
        
        return card

    def render_my_requests(self):
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
            if req.status == "Pending":
                s_text = "Waiting Confirmation"
            else:
                s_text = req.status
                if req.status == "Completed":
                    s_color, s_fg = "#DCFCE7", "#166534"
            ctk.CTkLabel(status_frame, text=s_text, fg_color=s_color, text_color=s_fg, corner_radius=10, width=150, height=30).pack()

            if req.status == "Completed":
                ctk.CTkButton(status_frame, text="Give Feedback", fg_color="#F6A836", hover_color="#E59930", text_color="white", cursor="hand2",
                               command=lambda r=req: self.open_feedback_popup(r)).pack(pady=10)

    def render_feedback(self):
        scroll = ctk.CTkScrollableFrame(self.content_frame, fg_color="transparent")
        scroll.pack(fill="both", expand=True, pady=20)
        feedbacks = Feedback.by_receiver(self.app.current_user.id)
        if not feedbacks:
            ctk.CTkLabel(scroll, text="No feedback yet.", text_color="gray").pack(pady=20)
            return
        for fb in feedbacks:
            card = ctk.CTkFrame(scroll, fg_color="white", border_width=1, border_color="#DDD")
            card.pack(fill="x", pady=10, ipadx=20, ipady=20)
            ctk.CTkLabel(card, text=f"To Provider #{fb.idProvider}", font=("Arial", 14, "bold"), text_color="#132A13").pack(anchor="w")
            ctk.CTkLabel(card, text="★" * fb.rating, text_color="#F6A836").pack(anchor="w")
            ctk.CTkLabel(card, text=fb.komentar, text_color="#555").pack(anchor="w", pady=(5, 0))

    def open_feedback_popup(self, req):
        popup = ctk.CTkToplevel(self)
        popup.title("Give Feedback")
        popup.transient(self)
        popup.grab_set()
        popup.resizable(False, False)
        frame = ctk.CTkFrame(popup, fg_color="#FFFFFF")
        frame.pack(padx=20, pady=20, fill="x")
        ctk.CTkLabel(frame, text="Rating (1-5)", text_color="#132A13").pack(anchor="w")
        rating_entry = ctk.CTkEntry(frame)
        rating_entry.pack(fill="x", pady=5)
        ctk.CTkLabel(frame, text="Comment", text_color="#132A13").pack(anchor="w")
        comment_entry = ctk.CTkEntry(frame)
        comment_entry.pack(fill="x", pady=5)

        def submit():
            try:
                rating = int(rating_entry.get().strip())
            except Exception:
                messagebox.showerror("Error", "Rating harus angka 1-3")
                return
            if rating not in [1,2,3,4,5]:
                messagebox.showerror("Error", "Rating harus 1-3")
                return
            komentar = comment_entry.get().strip()
            don = DataMakanan.find_by_id(req.idDonasi)
            if not don:
                messagebox.showerror("Error", "Data donasi tidak ditemukan")
                return
            res = FeedbackController.kirimFeedback(don.idProvider, self.app.current_user.id, rating, komentar)
            if res.get("status") == "SUCCESS":
                messagebox.showinfo("Success", "Feedback terkirim")
                popup.destroy()
                self.switch_menu("Feedback")
            else:
                messagebox.showerror("Error", res.get("message", "Gagal mengirim feedback"))

        ctk.CTkButton(frame, text="Submit", fg_color="#132A13", text_color="white", command=submit).pack(pady=10)

    def render_profile(self):
        user = self.app.current_user
        scroll = ctk.CTkScrollableFrame(self.content_frame, fg_color="transparent")
        scroll.pack(fill="both", expand=True)
        
        # Profile card
        card = ctk.CTkFrame(scroll, fg_color="white", corner_radius=15, border_width=1, border_color="#EEE")
        card.pack(fill="x", ipady=20, padx=5)
        
        def create_field(parent, label_text, value):
            row = ctk.CTkFrame(parent, fg_color="transparent")
            row.pack(fill="x", padx=30, pady=10)
            ctk.CTkLabel(
                row, 
                text=label_text, 
                font=("Arial", 14, "bold"), 
                text_color="#333", 
                width=150, 
                anchor="w"
            ).pack(side="left", anchor="n", pady=5)
            entry = ctk.CTkEntry(
                row, 
                height=40, 
                corner_radius=8, 
                fg_color="transparent", 
                border_color="#CCC", 
                text_color="#333"
            )
            entry.insert(0, value)
            entry.pack(side="left", fill="x", expand=True)
            return entry

        # Profile fields
        self.entry_name = create_field(card, "Name", user.nama)
        self.entry_phone = create_field(card, "Contact Number", user.noTelepon)
        self.entry_email = create_field(card, "Email", user.email)
        
        # Divider
        ctk.CTkFrame(card, height=1, fg_color="#EEE").pack(fill="x", pady=20, padx=30)
        
        # Password change section
        ctk.CTkLabel(
            card, 
            text="Change Password", 
            font=("Arial", 14, "bold"), 
            text_color="#333"
        ).pack(anchor="w", padx=30)
        
        self.entry_new_pass = ctk.CTkEntry(
            card, 
            placeholder_text="New Password (leave empty to keep current)", 
            show="*", 
            height=40, 
            corner_radius=8, 
            fg_color="transparent", 
            border_color="#CCC", 
            text_color="#333"
        )
        self.entry_new_pass.pack(fill="x", padx=(180, 30), pady=5)
        
        # Save button
        btn_row = ctk.CTkFrame(card, fg_color="transparent")
        btn_row.pack(fill="x", padx=30, pady=(30, 0))
        
        ctk.CTkButton(
            btn_row, 
            text="Save Changes ✓", 
            fg_color="#132A13", 
            hover_color="#1F381F", 
            text_color="white", 
            width=120, 
            height=35, 
            corner_radius=20, 
            command=self.save_profile
        ).pack(side="right")

    def save_profile(self):
        user = self.app.current_user
        
        # Validation
        if not self.entry_name.get().strip():
            messagebox.showerror("Error", "Name cannot be empty!")
            return
        
        if not self.entry_email.get().strip():
            messagebox.showerror("Error", "Email cannot be empty!")
            return
        
        try:
            # Update basic info
            user.nama = self.entry_name.get().strip()
            user.noTelepon = self.entry_phone.get().strip()
            user.email = self.entry_email.get().strip()
            
            # Update password if provided
            new_password = self.entry_new_pass.get()
            if new_password:
                user.password_hash = hashlib.sha256(new_password.encode()).hexdigest()
            
            # Save to database
            user.update()
            
            messagebox.showinfo("Success", "Profile updated successfully!")
            self.entry_new_pass.delete(0, 'end')
            self.refresh_content()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update profile: {str(e)}")

    def do_request(self, idDonasi):
        if messagebox.askyesno("Confirm", "Request this food?"):
            result = RequestController.buatRequest(idDonasi, self.app.current_user.id)
            if result.get("status") == "SUCCESS":
                messagebox.showinfo("Success", "Request sent!")
                self.switch_menu("My Requests")
            else:
                messagebox.showerror("Error", result.get("message", "Gagal request"))
