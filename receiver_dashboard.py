import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import os
from PIL import Image 

from src.output.side_menu import SideMenu
from src.controller.donasi_controller import DonasiController
from src.controller.request_controller import RequestController
from src.controller.feedback_controller import FeedbackController
from src.model.feedbackdonasi import Feedback
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
        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.grid(row=0, column=1, sticky="nsew")
        
        self.header_frame = ctk.CTkFrame(self.main_area, height=80, fg_color="white", corner_radius=0)
        self.header_frame.pack(side="top", fill="x")
        self.header_frame.pack_propagate(False)

        self.content_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.content_frame.pack(side="top", fill="both", expand=True, padx=20, pady=20)
        
        self.load_icons()

    def load_icons(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.join(script_dir, "../../src/assets") 
        icon_names = {"Available Foods": "active.png", "Active Requests": "newrequest.png", "Incoming": "delivery.png", "Total Completed": "completed.png"}
        for key, filename in icon_names.items():
            try:
                pil = Image.open(os.path.join(base_path, filename))
                self.icon_cache[key] = ctk.CTkImage(light_image=pil, dark_image=pil, size=(24, 24))
            except: self.icon_cache[key] = None 

    def show_dashboard(self):
        self.show_dashboard_ui()

    def show_dashboard_ui(self):
        if not getattr(self.app, "current_user", None): return

        if self.sidebar_frame: self.sidebar_frame.destroy()
        self.sidebar_frame = SideMenu(
            self, self.app, 
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
        for widget in self.content_frame.winfo_children(): widget.destroy()
        for widget in self.header_frame.winfo_children(): widget.destroy()

        if self.current_menu == "Dashboard":
            self.render_header("Dashboard", "Overview of your activity")
            self.render_overview()
        elif self.current_menu == "Available Food":
            self.render_header("Available Food", "Browse and request donations")
            self.render_available_food()
        elif self.current_menu == "My Requests":
            self.render_header("My Requests", "Track your food requests")
            self.render_my_requests()
        elif self.current_menu == "Feedback":
            self.render_header("Feedback", "History of your feedbacks")
            self.render_feedback()
        elif self.current_menu == "Profile":
            self.render_header("Profile", "Manage your profile settings")
            self.render_profile()

    # ============================================
    # HEADER (DIPERBAIKI)
    # ============================================
    def render_header(self, title, subtitle):
        left_c = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        left_c.pack(side="left", padx=30, pady=15)
        ctk.CTkLabel(left_c, text=title, font=("Arial", 24, "bold"), text_color="#132A13").pack(anchor="w")
        ctk.CTkLabel(left_c, text=subtitle, font=("Arial", 13), text_color="gray").pack(anchor="w")

        right_c = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        right_c.pack(side="right", padx=30)
        
        # Hapus Tombol Lonceng
        
        user = self.app.current_user
        initials = user.nama[:2].upper() if user.nama else "??"
        avatar = ctk.CTkFrame(right_c, width=40, height=40, corner_radius=20, fg_color="#132A13")
        avatar.pack(side="left", padx=10)
        ctk.CTkLabel(avatar, text=initials, text_color="#C5E064", font=("Arial", 14, "bold")).place(relx=0.5, rely=0.5, anchor="center")

        info = ctk.CTkFrame(right_c, fg_color="transparent")
        info.pack(side="left")
        # Rapatkan teks
        ctk.CTkLabel(info, text=user.nama, font=("Arial", 14, "bold"), text_color="#132A13").pack(anchor="w", pady=0)
        ctk.CTkLabel(info, text="Receiver", font=("Arial", 11), text_color="gray").pack(anchor="w", pady=0)

    def render_profile(self):
        user = self.app.current_user
        scroll = ctk.CTkScrollableFrame(self.content_frame, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        card = ctk.CTkFrame(scroll, fg_color="white", corner_radius=15, border_width=1, border_color="#EEE")
        card.pack(fill="x", ipady=20, padx=5)

        def create_field(parent, label_text, value):
            row = ctk.CTkFrame(parent, fg_color="transparent")
            row.pack(fill="x", padx=30, pady=10)
            ctk.CTkLabel(row, text=label_text, font=("Arial", 14, "bold"), text_color="#333", width=150, anchor="w").pack(side="left", anchor="n", pady=5)
            entry = ctk.CTkEntry(row, height=40, corner_radius=8, fg_color="transparent", border_color="#CCC", text_color="#333")
            entry.insert(0, value)
            entry.pack(side="left", fill="x", expand=True)
            return entry

        self.entry_name = create_field(card, "Name", user.nama)
        self.entry_phone = create_field(card, "Contact Number", user.noTelepon)
        self.entry_email = create_field(card, "Email", user.email)

        ctk.CTkFrame(card, height=1, fg_color="#EEE").pack(fill="x", pady=20, padx=30)
        ctk.CTkLabel(card, text="Change Password", font=("Arial", 14, "bold"), text_color="#333").pack(anchor="w", padx=30)
        
        self.entry_new_pass = ctk.CTkEntry(card, placeholder_text="New Password", show="*", height=40, corner_radius=8, fg_color="transparent", border_color="#CCC", text_color="#333")
        self.entry_new_pass.pack(fill="x", padx=(180, 30), pady=5)

        btn_row = ctk.CTkFrame(card, fg_color="transparent")
        btn_row.pack(fill="x", padx=30, pady=(30, 0))
        ctk.CTkButton(btn_row, text="Save ✓", fg_color="#132A13", hover_color="#1F381F", text_color="white", width=100, height=35, corner_radius=20, command=self.save_profile).pack(side="right")

    def save_profile(self):
        user = self.app.current_user
        user.nama = self.entry_name.get()
        user.noTelepon = self.entry_phone.get()
        user.email = self.entry_email.get()
        user.update()
        messagebox.showinfo("Success", "Profile updated!")
        self.render_header("Profile", "Manage your profile")

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

    def create_stat_card(self, parent, title, value):
        card = ctk.CTkFrame(parent, fg_color="#132A13", corner_radius=10)
        icon_bg = ctk.CTkFrame(card, width=40, height=40, corner_radius=20, fg_color="white")
        icon_bg.pack(anchor="w", padx=15, pady=(15, 5))
        
        img = self.icon_cache.get(title)
        if img: ctk.CTkLabel(icon_bg, text="", image=img).place(relx=0.5, rely=0.5, anchor="center")
        else: ctk.CTkLabel(icon_bg, text="?", text_color="#132A13").place(relx=0.5, rely=0.5, anchor="center")

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
            self.create_food_card(scroll, d).grid(row=i//3, column=i%3, padx=10, pady=10, sticky="nsew")

    def create_food_card(self, parent, donasi):
        card = ctk.CTkFrame(parent, fg_color="#132A13", corner_radius=15)
        ctk.CTkFrame(card, height=100, fg_color="#C5E064", corner_radius=10).pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(card, text=donasi.jenisMakanan, font=("Arial", 16, "bold"), text_color="white", anchor="w").pack(fill="x", padx=15)
        ctk.CTkLabel(card, text=f"Portions: {donasi.jumlahPorsi}", font=("Arial", 12), text_color="white", anchor="w").pack(fill="x", padx=15, pady=5)
        
        ctk.CTkButton(card, text="Request", fg_color="#F6A836", hover_color="#E59930", text_color="white", 
                      command=lambda: self.do_request(donasi.idDonasi)).pack(fill="x", padx=15, pady=(5, 15))
        return card

    def do_request(self, did):
        if messagebox.askyesno("Confirm", "Request food?"):
            res = RequestController.buatRequest(did, self.app.current_user.id)
            if res["status"]=="SUCCESS": 
                messagebox.showinfo("Success", "Request sent!")
                self.switch_menu("My Requests")
            else: messagebox.showerror("Error", res["message"])

    def render_my_requests(self):
        scroll = ctk.CTkScrollableFrame(self.content_frame, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        my_reqs = [r for r in RequestController.semuaRequest() if str(r.idReceiver) == str(self.app.current_user.id)]
        
        for req in my_reqs:
            card = ctk.CTkFrame(scroll, fg_color="white", corner_radius=10)
            card.pack(fill="x", pady=5)
            
            info = ctk.CTkFrame(card, fg_color="transparent")
            info.pack(side="left", padx=20, pady=15)
            ctk.CTkLabel(info, text=f"Request #{req.idRequest}", font=("Arial", 14, "bold"), text_color="#333").pack(anchor="w")
            d_name = RequestController.getDonasiName(req.idDonasi)
            ctk.CTkLabel(info, text=d_name, text_color="gray").pack(anchor="w")

            status = ctk.CTkFrame(card, fg_color="transparent")
            status.pack(side="right", padx=20)
            
            if req.status == "Completed":
                ctk.CTkButton(status, text="Rate / Feedback", fg_color="#10B981", text_color="white", width=120,
                              command=lambda r=req: self.popup_feedback(r)).pack(side="right")
            else:
                s_col = "#FEF9C3" if req.status=="Pending" else "#E0F2FE"
                s_txt = "#A16207" if req.status=="Pending" else "#075985"
                ctk.CTkLabel(status, text=req.status, fg_color=s_col, text_color=s_txt, corner_radius=10, width=100).pack()

    def popup_feedback(self, req):
        FeedbackPopup(self.app.master, req, self.app.current_user.id)

    def render_feedback(self):
        ctk.CTkLabel(self.content_frame, text="Feedback functionality focused on giving ratings in 'My Requests'.").pack(pady=20)

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
        
        self.slider = ctk.CTkSlider(self, from_=1, to=5, number_of_steps=4)
        self.slider.pack(pady=10)
        self.slider.set(5)
        
        self.lbl_val = ctk.CTkLabel(self, text="5 Stars")
        self.lbl_val.pack()
        self.slider.configure(command=lambda v: self.lbl_val.configure(text=f"{int(v)} Stars"))

        self.txt_comment = ctk.CTkTextbox(self, height=100, width=300)
        self.txt_comment.pack(pady=10)
        
        ctk.CTkButton(self, text="Submit", fg_color="#132A13", command=self.submit).pack(pady=10)

    def submit(self):
        rating = int(self.slider.get())
        comment = self.txt_comment.get("1.0", "end").strip()
        res = FeedbackController.kirimFeedback(self.provider_id, self.receiver_id, rating, comment)
        if res["status"] == "SUCCESS":
            messagebox.showinfo("Thanks", "Feedback sent!")
            self.destroy()
        else:
            messagebox.showerror("Error", "Failed to send feedback")