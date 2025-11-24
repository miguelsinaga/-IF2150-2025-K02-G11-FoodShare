import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from datetime import datetime, date 
from PIL import Image
import os 
import functools 

# Pastikan path import ini benar di proyek Anda
from src.output.side_menu import SideMenu
from src.controller.donasi_controller import DonasiController
from src.controller.request_controller import RequestController
from src.controller.feedback_controller import FeedbackController
from src.model.feedbackdonasi import Feedback
from src.model.reqdonasi import RequestDonasi

class ProviderDashboard(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="#F6F6F6")
        self.app = app
        self.current_menu = "Dashboard"
        self.request_filter = "All"
        self.icon_cache = {} 

        # Layout utama: Grid 2 kolom (Sidebar, Content)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar_frame = None
        
        # Content Container
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        # Menggunakan pack di sini agar frame content mengisi area grid(0,1)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        # Pre-load icons
        self.load_icons()

    def load_icons(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.join(script_dir, "../../src/assets") 
        
        icon_names = {
            "Active Stocks": "active.png",
            "New Requests": "newrequest.png",
            "On Delivery": "delivery.png",
            "Total Donations": "completed.png"
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


    def show_dashboard_ui(self):
        if not getattr(self.app, "current_user", None): return

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

        for widget in self.content_frame.winfo_children():
            widget.destroy()

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

    def show_dashboard(self):
        self.show_dashboard_ui()

    # ==============================================================
    # 1. DASHBOARD OVERVIEW 
    # ==============================================================
    def render_overview(self):
        user = self.app.current_user
        
        ctk.CTkLabel(self.content_frame, text=f"Hi, {user.nama}!", 
                     font=("Arial", 24, "bold"), text_color="#132A13").pack(anchor="w")
        ctk.CTkLabel(self.content_frame, text="Here's an overview of your FoodShare activities today.", 
                     font=("Arial", 14), text_color="gray").pack(anchor="w", pady=(0, 20))

        try:
             all_donasi_raw = DonasiController.semuaDonasi()
        except AttributeError:
             all_donasi_raw = DonasiController.getDonasiAktif()
        
        my_all_donasi = []
        for d in all_donasi_raw:
            d_provider_id = getattr(d, 'idProvider', getattr(d, 'provider_id', getattr(d, 'id_provider', None)))
            
            if d_provider_id is not None and str(d_provider_id) == str(user.id):
                if getattr(d, 'status', '').lower() not in ["completed", "cancelled"]:
                    my_all_donasi.append(d)

        my_donasi_ids = [d.idDonasi for d in my_all_donasi]
        
        all_requests = RequestController.semuaRequest()
        my_requests = [req for req in all_requests if req.idDonasi in my_donasi_ids]
        
        count_active_stocks = sum(1 for d in my_all_donasi if getattr(d, 'status', 'N/A') == "Tersedia")
        count_pending = sum(1 for req in my_requests if req.status == "Pending")
        count_on_delivery = sum(1 for req in my_requests if req.status == "On Delivery")
        count_completed = sum(1 for req in RequestController.getRequestByProviderId(user.id) if req.status == "Completed")
        
        stats_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        stats_frame.pack(fill="x", pady=10)

        self.create_stat_card(stats_frame, "Active Stocks", str(count_active_stocks), "#132A13").pack(side="left", expand=True, fill="x", padx=5)
        self.create_stat_card(stats_frame, "New Requests", str(count_pending), "#132A13").pack(side="left", expand=True, fill="x", padx=5)
        self.create_stat_card(stats_frame, "On Delivery", str(count_on_delivery), "#132A13").pack(side="left", expand=True, fill="x", padx=5)
        self.create_stat_card(stats_frame, "Total Donations", str(count_completed), "#132A13").pack(side="left", expand=True, fill="x", padx=5)

        banner = ctk.CTkFrame(self.content_frame, fg_color="#DCEE85", corner_radius=10)
        banner.pack(fill="x", pady=30, ipady=10)
        ctk.CTkLabel(banner, text="♻ You've helped share meals this month.", 
                     text_color="#132A13", font=("Arial", 16, "bold")).pack(anchor="w", padx=20)


    def create_stat_card(self, parent, title, value, bg_color):
        card = ctk.CTkFrame(parent, fg_color=bg_color, corner_radius=10)
        
        icon_bg = ctk.CTkFrame(card, width=40, height=40, corner_radius=20, fg_color="white")
        icon_bg.pack(anchor="w", padx=15, pady=(15, 5))
        
        ctk_image = self.icon_cache.get(title)
        
        if ctk_image:
            icon_label = ctk.CTkLabel(icon_bg, text="", image=ctk_image)
            icon_label.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        else:
            ctk.CTkLabel(icon_bg, text="?", text_color="#132A13", font=("Arial", 16, "bold")).place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        ctk.CTkLabel(card, text=title, font=("Arial", 12), text_color="#A0B0A0").pack(anchor="w", padx=15)
        ctk.CTkLabel(card, text=value, font=("Arial", 28, "bold"), text_color="white").pack(anchor="w", padx=15, pady=(0, 15))
        return card

    # ==============================================================
    # 2. FOOD STOCK (Revisi ke Pack dengan Lebar Tetap)
    # ==============================================================
    def render_food_stock(self):
        header_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(header_frame, text="Available Food Items", font=("Arial", 20, "bold"), text_color="#132A13").pack(side="left")
        
        ctk.CTkButton(header_frame, text="+ Add Availability", font=("Arial", 13, "bold"),
                      fg_color="#F6A836", hover_color="#E59930", text_color="white",
                      cursor="hand2", 
                      command=self.popup_add_donasi).pack(side="right") 

        table_frame = ctk.CTkScrollableFrame(self.content_frame, fg_color="white", corner_radius=10)
        table_frame.pack(fill="both", expand=True)

        headers = ["Food Item", "Expiration", "Portions", "Status", "Action"]
        self.create_table_header(table_frame, headers)

        try:
             all_donasi_raw = DonasiController.semuaDonasi()
        except AttributeError:
             all_donasi_raw = DonasiController.getDonasiAktif()
        
        current_user_id = str(self.app.current_user.id)
        
        my_all_donasi = []
        for item in all_donasi_raw:
            p_id = getattr(item, 'idProvider', getattr(item, 'provider_id', getattr(item, 'id_provider', None)))
            
            if p_id is not None and str(p_id) == current_user_id:
                if getattr(item, 'status', '').lower() not in ["completed", "cancelled"]:
                    my_all_donasi.append(item)

        if not my_all_donasi:
            ctk.CTkLabel(table_frame, text="No active food stock found.", text_color="gray").pack(pady=20)
        else:
            for item in my_all_donasi:
                self.create_stock_row(table_frame, item)

    def create_stock_row(self, parent, item):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=10)
        
        # Lebar Kolom (Sama dengan header: 200, 130, 90, 110, 180)
        widths = [200, 130, 90, 110, 180] 

        # Food Item
        ctk.CTkLabel(row, text=item.jenisMakanan, font=("Arial", 13), width=widths[0], anchor="w", text_color="#333").pack(side="left", padx=10)
        # Expiration
        ctk.CTkLabel(row, text=item.batasWaktu, font=("Arial", 13), width=widths[1], anchor="w", text_color="#333").pack(side="left", padx=10)
        # Portions
        ctk.CTkLabel(row, text=str(item.jumlahPorsi), font=("Arial", 13), width=widths[2], anchor="w", text_color="#333").pack(side="left", padx=10)
        
        # Status Badge
        status_text = getattr(item, 'status', 'N/A')
        
        if status_text == "Tersedia":
            status_color = "#E6F4EA"
            status_text_color = "#1E8E3E"
            display_text = "Active"
        elif status_text == "Dipesan" or status_text == "Dikirim" or status_text == "Preparing":
            status_color = "#FEF9C3"
            status_text_color = "#A16207"
            display_text = status_text
        else:
            status_color = "#FCE8E6"
            status_text_color = "#D93025"
            display_text = status_text
            
        status_lbl = ctk.CTkLabel(row, text=display_text, 
                                  fg_color=status_color, text_color=status_text_color, corner_radius=15, width=90)
        status_lbl.pack(side="left", padx=10) 

        # Actions Frame (diberi lebar yang tersisa)
        action_frame = ctk.CTkFrame(row, fg_color="transparent", width=widths[4])
        action_frame.pack(side="left", fill="x", padx=10)
        
        # Actions 
        btn_edit = ctk.CTkButton(action_frame, text="Edit", width=60, fg_color="white", border_width=1, border_color="#DDD", 
                                 text_color="#333", hover_color="#F0F0F0", cursor="hand2",
                                 command=lambda item=item: self.popup_edit_donasi(item)) 
        btn_edit.pack(side="left", padx=5)
        
        btn_del = ctk.CTkButton(action_frame, text="Remove", width=70, fg_color="white", border_width=1, border_color="#EF4444", 
                                 text_color="#EF4444", hover_color="#FEF2F2", cursor="hand2",
                                 command=lambda item=item: self.hapus_donasi(item.idDonasi))
        btn_del.pack(side="left", padx=5)
        
        ctk.CTkFrame(parent, height=1, fg_color="#EEE").pack(fill="x")

    def popup_add_donasi(self):
        AddDonasiPopup(self.app.master, self.app, self.show_dashboard_ui)

    def popup_edit_donasi(self, item_to_edit):
        AddDonasiPopup(self.app.master, self.app, self.show_dashboard_ui, item_to_edit=item_to_edit)
        
    def hapus_donasi(self, idDonasi):
        if messagebox.askyesno("Confirm", "Delete this item?"):
            result = DonasiController.batalkanDonasi(idDonasi)
            if result and result.get("status") == "SUCCESS":
                messagebox.showinfo("Success", result.get("message", "Donation cancelled successfully."))
            else:
                messagebox.showerror("Error", result.get("message", "Failed to cancel donation."))
            self.show_dashboard_ui()


    # ==============================================================
    # 3. FOOD REQUESTS (Revisi ke Pack dengan Lebar Tetap)
    # ==============================================================
    def set_request_filter(self, status):
        self.request_filter = status
        self.render_food_requests()

    def handle_request_action(self, request_id: int, action: str):
        if action == "Accept":
            new_status = "Preparing"
        elif action == "Reject":
            new_status = "Rejected"
        elif action == "Ready for Delivery":
            new_status = "On Delivery"
        else:
            messagebox.showerror("Error", "Aksi tidak dikenal.")
            return

        result = RequestController.updateStatus(request_id, new_status)
        
        if result["status"] == "SUCCESS":
            messagebox.showinfo("Success", result["message"])
            self.render_food_requests()
        else:
            messagebox.showerror("Error", result["message"])


    def render_food_requests(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        user_id = self.app.current_user.id
        
        ctk.CTkLabel(self.content_frame, text="All Requests", font=("Arial", 20, "bold"), text_color="#132A13").pack(anchor="w", pady=(0, 20))

        filter_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        filter_frame.pack(anchor="w", pady=(0, 20))
        
        filter_map = {
            "All": "All", 
            "Requested": "Pending", 
            "Preparing": "Preparing", 
            "On Delivery": "On Delivery", 
            "Completed": "Completed"
        }
        
        for ui_label, status_value in filter_map.items():
            is_active = (status_value == self.request_filter) 
            fg = "#132A13" if is_active else "white"
            tc = "white" if is_active else "#132A13"
            hover = "#1F381F" if is_active else "#F0F0F0"
            
            ctk.CTkButton(
                filter_frame, 
                text=ui_label, 
                fg_color=fg, 
                text_color=tc, 
                width=100, 
                corner_radius=20, 
                border_width=1, 
                border_color="#DDD",
                hover_color=hover, 
                cursor="hand2",
                command=lambda s=status_value: self.set_request_filter(s)
            ).pack(side="left", padx=5)

        table_frame = ctk.CTkScrollableFrame(self.content_frame, fg_color="white", corner_radius=10)
        table_frame.pack(fill="both", expand=True)

        headers = ["Req ID", "Food Item", "Receiver", "Date", "Status", "Action"]
        self.create_table_header(table_frame, headers)

        all_requests_by_provider = RequestController.getRequestByProviderId(user_id)

        filtered_requests = all_requests_by_provider
        if self.request_filter != "All":
            filtered_requests = [
                req for req in all_requests_by_provider if req.status == self.request_filter
            ]

        if not filtered_requests:
              ctk.CTkLabel(table_frame, text="Tidak ada permintaan makanan untuk saat ini.", font=("Arial", 14), text_color="gray").pack(pady=20)
        else:
            for req in filtered_requests:
                self.create_request_row(table_frame, req)

    def create_request_row(self, parent, req: RequestDonasi):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=5)
        
        # Lebar Kolom (Sama dengan header: 70, 180, 120, 100, 100, 180)
        widths = [70, 180, 120, 100, 100, 180] 

        # Req ID
        ctk.CTkLabel(row, text=f"REQ{req.idRequest}", width=widths[0], anchor="w", text_color="#333").pack(side="left", padx=10)
        
        # Food Item 
        food_name = RequestController.getDonasiName(req.idDonasi)
        ctk.CTkLabel(row, text=food_name, width=widths[1], anchor="w", text_color="#333").pack(side="left", padx=10)
        
        # Receiver
        receiver_name = RequestController.getReceiverName(req.idReceiver)
        ctk.CTkLabel(row, text=receiver_name, width=widths[2], anchor="w", text_color="#333").pack(side="left", padx=10)
        
        # Date
        ctk.CTkLabel(row, text=req.tanggalRequest[:10], width=widths[3], anchor="w", text_color="#333").pack(side="left", padx=10)

        # Status Badge
        status_colors = { 
            "Pending": ("#FEF9C3", "#A16207"), 
            "Preparing": ("#E0F2FE", "#075985"), 
            "On Delivery": ("#DBEAFE", "#1E40AF"), 
            "Completed": ("#DCFCE7", "#166534"), 
            "Rejected": ("#FEE2E2", "#B91C1C"), 
        }
        s_color, s_text = status_colors.get(req.status, ("#F3F4F6", "#6B7280"))
        
        ctk.CTkLabel(row, text=req.status, fg_color=s_color, text_color=s_text, corner_radius=15, width=90).pack(side="left", padx=10)

        # Action Frame (diberi lebar yang tersisa)
        action_frame = ctk.CTkFrame(row, fg_color="transparent", width=widths[5])
        action_frame.pack(side="left", fill="x", padx=10)

        # Konten Action Frame (Menggunakan Pack)
        if req.status == "Pending":
            ctk.CTkButton(action_frame, text="Accept", width=70, fg_color="#10B981", hover_color="#059669", text_color="white", cursor="hand2", command=lambda: self.handle_request_action(req.idRequest, "Accept")).pack(side="left", padx=2)
            ctk.CTkButton(action_frame, text="Reject", width=70, fg_color="white", border_width=1, border_color="red", text_color="red", hover_color="#FEF2F2", cursor="hand2", command=lambda: self.handle_request_action(req.idRequest, "Reject")).pack(side="left", padx=2)
            
        elif req.status == "Preparing":
            ctk.CTkButton(action_frame, text="Ready for Delivery", width=150, fg_color="#4D70B9", hover_color="#4D70B9", text_color="white", cursor="hand2", command=lambda: self.handle_request_action(req.idRequest, "Ready for Delivery")).pack(side="left", padx=2)
            
        elif req.status == "On Delivery":
            ctk.CTkLabel(action_frame, text="Waiting for Receiver", text_color="gray").pack(side="left", padx=2)
            
        elif req.status in ["Completed", "Rejected"]:
            ctk.CTkLabel(action_frame, text="No Action Needed", text_color="gray").pack(side="left", padx=2)
            
        ctk.CTkFrame(parent, height=1, fg_color="#EEE").pack(fill="x")


    # ==============================================================
    # 4. FEEDBACK & 5. PROFILE (Tidak ada perubahan)
    # ==============================================================
    def render_feedback(self):
        ctk.CTkLabel(self.content_frame, text="Feedback", font=("Arial", 20, "bold"), text_color="#132A13").pack(anchor="w")
        ctk.CTkLabel(self.content_frame, text="See what receivers think about your donations", text_color="gray").pack(anchor="w", pady=(0, 20))
        
        summary = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=10, border_width=1, border_color="#DDD")
        summary.pack(fill="x", pady=(0, 20), ipadx=20, ipady=20)
        
        ctk.CTkLabel(summary, text="3.7", font=("Arial", 40, "bold"), text_color="#F6A836").pack(side="left", padx=20)
        star_frame = ctk.CTkFrame(summary, fg_color="transparent")
        star_frame.pack(side="left")
        ctk.CTkLabel(star_frame, text="★ ★ ★ ★ ☆", font=("Arial", 20), text_color="#F6A836").pack(anchor="w")
        ctk.CTkLabel(star_frame, text="Based on feedbacks", text_color="gray").pack(anchor="w")

        scroll = ctk.CTkScrollableFrame(self.content_frame, fg_color="transparent")
        scroll.pack(fill="both", expand=True)
        
        try:
            feedbacks = Feedback.by_provider(self.app.current_user.id)
        except AttributeError:
            ctk.CTkLabel(scroll, text="No feedbacks available.", text_color="gray").pack(pady=20)
            return

        for fb in feedbacks:
            card = ctk.CTkFrame(scroll, fg_color="white", corner_radius=10, border_width=1, border_color="#DDD")
            card.pack(fill="x", pady=10, ipadx=15, ipady=15)
            h = ctk.CTkFrame(card, fg_color="transparent")
            h.pack(fill="x")
            ctk.CTkLabel(h, text=f"Receiver #{fb.idReceiver}", font=("Arial", 14, "bold"), text_color="#333").pack(side="left")
            ctk.CTkLabel(h, text="★"*fb.rating, text_color="#F6A836").pack(side="right")
            ctk.CTkLabel(card, text=fb.komentar, font=("Arial", 14), text_color="#555", anchor="w", justify="left").pack(fill="x", pady=(10, 0))

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
        
        ctk.CTkButton(btn_frame, text="Save", fg_color="#132A13", hover_color="#1F381F", text_color="white", width=100, cursor="hand2").pack(side="right")
        ctk.CTkButton(btn_frame, text="Cancel", fg_color="white", border_width=1, border_color="#333", text_color="#333", hover_color="#F0F0F0", width=100, cursor="hand2").pack(side="right", padx=10)

    def create_profile_field(self, parent, label, value):
        ctk.CTkLabel(parent, text=label, font=("Arial", 12, "bold"), text_color="#333").pack(anchor="w", pady=(10, 5))
        entry = ctk.CTkEntry(parent, width=400)
        entry.insert(0, value)
        entry.pack(anchor="w")

    # ==============================================================
    # FUNGSI: create_table_header (Direvisi ke Pack dengan Lebar Tetap)
    # ==============================================================
    def create_table_header(self, parent, headers):
        header_frame = ctk.CTkFrame(parent, fg_color="#F9FAFB", height=40)
        header_frame.pack(fill="x")
        
        # Lebar kolom (Total width sekitar 750px)
        if len(headers) == 6: 
            # Req ID | Food Item | Receiver | Date | Status | Action (Requests)
            widths = [70, 180, 120, 100, 100, 180] 
        elif len(headers) == 5:
            # Food Item | Expiration | Portions | Status | Action (Stock)
            widths = [200, 130, 90, 110, 180] 
        else:
            widths = [150] * len(headers) 

        for i, h in enumerate(headers):
            ctk.CTkLabel(header_frame, text=h, font=("Arial", 12, "bold"), 
                         width=widths[i], anchor="w", text_color="#666").pack(side="left", padx=10)
            
        ctk.CTkFrame(parent, height=1, fg_color="#DDD").pack(fill="x")


class AddDonasiPopup(ctk.CTkToplevel):
    def __init__(self, parent, app_instance, refresh_callback, item_to_edit=None):
        super().__init__(parent)
        
        self.app = app_instance 
        self.provider_id = self.app.current_user.id
        self.refresh_callback = refresh_callback
        self.item_to_edit = item_to_edit
        
        if self.item_to_edit:
            self.title("Edit Food Availability")
            self.mode = "edit"
        else:
            self.title("Add New Food Availability")
            self.mode = "add"

        self.transient(parent) 
        self.wait_visibility() 
        self.grab_set()
        self.resizable(False, False)
        
        window_width = 500
        window_height = 500
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.geometry(f'{window_width}x{window_height}+{x}+{y}')
        
        self.configure(fg_color="#F6F6F6")
        
        self.create_widgets()

    def create_widgets(self):
        header = ctk.CTkFrame(self, fg_color="#132A13", corner_radius=0)
        header.pack(fill="x", ipady=10)
        ctk.CTkLabel(header, text=f"{'Edit' if self.mode == 'edit' else 'Add'} Food Stock", 
                     font=("Arial", 18, "bold"), text_color="white").pack(pady=5)
        
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(padx=20, pady=20, fill="x")

        ctk.CTkLabel(content, text="Food Item Name", font=("Arial", 12, "bold"), text_color="#333").pack(anchor="w", pady=(5, 0))
        self.entry_jenis = ctk.CTkEntry(content, width=450, placeholder_text="e.g. Nasi Goreng, Roti Tawar")
        self.entry_jenis.pack(anchor="w", pady=(0, 10))

        ctk.CTkLabel(content, text="Portions Available", font=("Arial", 12, "bold"), text_color="#333").pack(anchor="w", pady=(5, 0))
        self.entry_porsi = ctk.CTkEntry(content, width=450, placeholder_text="Enter number of portions")
        self.entry_porsi.pack(anchor="w", pady=(0, 10))

        ctk.CTkLabel(content, text="Pickup Location (Address)", font=("Arial", 12, "bold"), text_color="#333").pack(anchor="w", pady=(5, 0))
        self.entry_lokasi = ctk.CTkEntry(content, width=450, placeholder_text="Input Location")
        self.entry_lokasi.pack(anchor="w", pady=(0, 10))
        
        ctk.CTkLabel(content, text="Expiration Date (YYYY-MM-DD)", font=("Arial", 12, "bold"), text_color="#333").pack(anchor="w", pady=(5, 0))
        self.entry_batas = ctk.CTkEntry(content, width=450, placeholder_text=date.today().strftime("%Y-%m-%d"))
        self.entry_batas.pack(anchor="w", pady=(0, 20))
        
        if self.mode == "edit":
            self.entry_jenis.insert(0, self.item_to_edit.jenisMakanan)
            self.entry_porsi.insert(0, str(self.item_to_edit.jumlahPorsi) if self.item_to_edit.jumlahPorsi is not None else "")
            self.entry_lokasi.delete(0, 'end') 
            self.entry_lokasi.insert(0, self.item_to_edit.lokasi)
            self.entry_batas.insert(0, self.item_to_edit.batasWaktu)
        
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkButton(btn_frame, text="Cancel", fg_color="white", border_width=1, border_color="#333", text_color="#333", hover_color="#F0F0F0", width=100, command=self.destroy).pack(side="right", padx=10)
        
        button_text = "Update Stock" if self.mode == "edit" else "Save Stock"
        ctk.CTkButton(btn_frame, text=button_text, fg_color="#F6A836", hover_color="#E59930", 
                      text_color="white", width=100, command=self.save_or_update_donasi).pack(side="right")
        
    def save_or_update_donasi(self):
        try:
            from src.controller.donasi_controller import DonasiController 

            jenis = self.entry_jenis.get().strip()
            porsi = self.entry_porsi.get().strip()
            lokasi = self.entry_lokasi.get().strip()
            batas = self.entry_batas.get().strip()

            if not all([jenis, porsi, lokasi, batas]):
                messagebox.showerror("Error", "Semua kolom harus diisi.")
                return

            try:
                porsi_int = int(porsi)
            except ValueError:
                messagebox.showerror("Error", "Jumlah Porsi harus berupa angka.")
                return
            
            datetime.strptime(batas, "%Y-%m-%d")

            data = {
                "jenisMakanan": jenis,
                "jumlahPorsi": porsi_int,
                "lokasi": lokasi,
                "batasWaktu": batas
            }

            if self.mode == "add":
                result = DonasiController.buatDonasi(self.provider_id, data)
                success_msg = "Food stock berhasil ditambahkan!"
            else:
                data["idDonasi"] = self.item_to_edit.idDonasi
                result = DonasiController.updateDonasi(data)
                success_msg = "Food stock berhasil diperbarui!"

            if result["status"] == "SUCCESS":
                messagebox.showinfo("Success", success_msg)
                self.destroy()
                self.refresh_callback() 
            else:
                messagebox.showerror("Error", f"Gagal memproses stock: {result['message']}")

        except ValueError as e:
            if "strptime" in str(e):
                messagebox.showerror("Error", "Format tanggal tidak valid. Gunakan YYYY-MM-DD.")
            else:
                messagebox.showerror("Error", f"Terjadi kesalahan tak terduga: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan tak terduga: {e}")