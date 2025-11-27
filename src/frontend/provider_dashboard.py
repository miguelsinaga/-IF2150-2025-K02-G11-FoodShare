import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from datetime import datetime, date
import calendar
from PIL import Image
import os
import functools

# Imports
from src.frontend.side_menu import SideMenu
from src.controller.donasi_controller import DonasiController
from src.controller.request_controller import RequestController
from src.controller.feedback_controller import FeedbackController
from src.model.feedbackdonasi import Feedback
from src.model.reqdonasi import RequestDonasi
# Mengambil konstanta lokasi dari File 1
from src.constants.locations import BANDUNG_LOCATIONS 

class ProviderDashboard(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="#F6F6F6")
        self.app = app
        self.current_menu = "Dashboard"
        self.request_filter = "All"
        self.icon_cache = {} 

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar_frame = None
        
        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.grid(row=0, column=1, sticky="nsew")
        
        self.header_frame = ctk.CTkFrame(self.main_area, height=80, fg_color="#FFFFFF", corner_radius=0)
        self.header_frame.pack(side="top", fill="x")
        self.header_frame.pack_propagate(False)
        
        # Shadow separator line
        ctk.CTkFrame(self.main_area, height=2, fg_color="#E5E7EB").pack(side="top", fill="x")

        self.content_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.content_frame.pack(side="top", fill="both", expand=True, padx=20, pady=20)
        
        self.load_icons()

    def load_icons(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.join(script_dir, "../../img") 
        
        icon_names = {
            "Active Stocks": "active.png",
            "New Requests": "newrequest.png",
            "On Delivery": "delivery.png",
            "Total Donations": "completed.png",
            "Total Portions Shared": "completed.png" # Fallback icon
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

        self.refresh_content()

    def refresh_content(self):
        # 1. Update User Data
        try:
            from src.model.user import Pengguna
            self.app.current_user = Pengguna.find_by_id(self.app.current_user.id) or self.app.current_user
        except Exception:
            pass
            
        # 2. Check Basic Ban Status
        try:
            if str(getattr(self.app.current_user, "status", "")).lower() == "banned":
                from tkinter import messagebox
                messagebox.showerror("Akun Diblokir", "Akun Anda diblokir dan tidak dapat menggunakan dashboard.")
                self.app.current_user = None
                self.app.show_frame("LoginPage")
                return
        except Exception:
            pass

        # 3. Check Provider Specific Role Status (From File 2 - Lebih Aman)
        try:
            if str(getattr(self.app.current_user, "role", "")).lower() == "provider":
                from src.backend.donatur_data import DonaturRepo
                dr = DonaturRepo().find_by_user_id(self.app.current_user.id)
                if dr and str(dr.get("status_akun","aktif")).lower() != "aktif":
                    from tkinter import messagebox
                    messagebox.showerror("Akun Diblokir", "Akun provider Anda diblokir oleh admin.")
                    self.app.current_user = None
                    self.app.show_frame("LoginPage")
                    return
        except Exception:
            pass

        for widget in self.content_frame.winfo_children(): widget.destroy()
        for widget in self.header_frame.winfo_children(): widget.destroy()

        if self.current_menu == "Dashboard":
            self.render_header("Dashboard", "Overview of your activity")
            self.render_overview()
        elif self.current_menu == "Food Stock":
            self.render_header("Food Stock", "Manage your available donations")
            self.render_food_stock()
        elif self.current_menu == "Food Requests":
            self.render_header("Food Requests", "Handle incoming requests")
            self.render_food_requests()
        elif self.current_menu == "Feedback":
            self.render_header("Feedback", "See what people say")
            self.render_feedback()
        elif self.current_menu == "Profile":
            self.render_header("Profile", "Manage your profile settings here")
            self.render_profile()

    def render_header(self, title, subtitle):
        left_c = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        left_c.pack(side="left", padx=30, pady=15)
        ctk.CTkLabel(left_c, text=title, font=("Arial", 24, "bold"), text_color="#132A13").pack(anchor="w")
        ctk.CTkLabel(left_c, text=subtitle, font=("Arial", 13), text_color="gray").pack(anchor="w")

        right_c = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        right_c.pack(side="right", padx=30)

        user = self.app.current_user
        initials = user.nama[:2].upper() if user.nama else "??"
        
        avatar = ctk.CTkButton(right_c, width=40, height=40, corner_radius=20, fg_color="#132A13", 
                               hover_color="#1F381F", text=initials, text_color="#C5E064", 
                               font=("Arial", 14, "bold"), cursor="hand2",
                               command=lambda: self.switch_menu("Profile"))
        avatar.pack(side="left", padx=10)

        info = ctk.CTkFrame(right_c, fg_color="transparent")
        info.pack(side="left")
        
        ctk.CTkLabel(info, text=user.nama, font=("Arial", 14, "bold"), text_color="#132A13").pack(anchor="w", pady=0)
        ctk.CTkLabel(info, text="Provider", font=("Arial", 11), text_color="gray").pack(anchor="w", pady=0)

    def switch_menu(self, menu_name):
        self.current_menu = menu_name
        self.show_dashboard_ui()

    def show_dashboard(self):
        self.show_dashboard_ui()

    # ==============================================================
    # 1. DASHBOARD OVERVIEW (Merged Logic)
    # ==============================================================
    def render_overview(self):
        user = self.app.current_user

        # Fetch Data
        try:
            all_donasi_raw = DonasiController.semuaDonasi()
        except Exception:
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
        
        # Calculate Counts
        count_active_stocks = sum(1 for d in my_all_donasi if getattr(d, 'status', 'N/A') == "Tersedia")
        count_pending = sum(1 for req in my_requests if req.status == "Pending")
        count_on_delivery = sum(1 for req in my_requests if req.status == "On Delivery")
        
        # Calculate Portions (Logic from File 2 - More detailed)
        completed_or_sent = [req for req in RequestController.getRequestByProviderId(user.id) if req.status in ("Completed", "FeedbackSent")]
        now = datetime.now()

        def get_portion(req):
            try:
                # Assuming DonasiController or similar can fetch by ID, 
                # or use existing list if optimized. Here using rudimentary lookup check
                # Note: In real app, cleaner to use Controller.
                from src.model.donasi import DataMakanan
                don = DataMakanan.find_by_id(req.idDonasi)
                return int(getattr(don, 'jumlahPorsi', 0)) if don else 0
            except Exception:
                return 0

        portions_by_month = {}
        total_portions = 0
        
        for r in completed_or_sent:
            p = get_portion(r)
            total_portions += p
            try:
                if isinstance(r.tanggalRequest, (datetime, date)):
                    mk = f"{r.tanggalRequest.year:04d}-{r.tanggalRequest.month:02d}"
                else:
                    mk = str(r.tanggalRequest)[:7]
            except Exception:
                mk = "unknown"
            portions_by_month[mk] = portions_by_month.get(mk, 0) + p
            
        current_month_key = f"{now.year:04d}-{now.month:02d}"
        portions_this_month = portions_by_month.get(current_month_key, 0)
        months_with_data = len([k for k in portions_by_month.keys() if k != "unknown"]) or 1
        avg_monthly_portions = total_portions / months_with_data
        
        # --- UI RENDER ---
        stats_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        stats_frame.pack(fill="x", pady=10)

        self.create_stat_card(stats_frame, "Active Stocks", str(count_active_stocks), "#132A13").pack(side="left", expand=True, fill="x", padx=5)
        self.create_stat_card(stats_frame, "New Requests", str(count_pending), "#132A13").pack(side="left", expand=True, fill="x", padx=5)
        self.create_stat_card(stats_frame, "On Delivery", str(count_on_delivery), "#132A13").pack(side="left", expand=True, fill="x", padx=5)
        # Using Total Portions from File 2 as it's a better metric than just raw donation count
        self.create_stat_card(stats_frame, "Total Portions Shared", str(total_portions), "#132A13").pack(side="left", expand=True, fill="x", padx=5)

        banner = ctk.CTkFrame(self.content_frame, fg_color="#DCEE85", corner_radius=10)
        banner.pack(fill="x", pady=30, ipady=10)
        ctk.CTkLabel(banner, text=f"♻ You've shared {portions_this_month} portions this month.", 
                     text_color="#132A13", font=("Arial", 16, "bold")).pack(anchor="w", padx=20)

        # Portion Summary (From File 2)
        summary = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=10)
        summary.pack(fill="x", pady=10)
        ctk.CTkLabel(summary, text="Portion Summary", font=("Arial", 18, "bold"), text_color="#132A13").pack(anchor="w", padx=20, pady=(15, 5))
        row1 = ctk.CTkFrame(summary, fg_color="transparent")
        row1.pack(fill="x", padx=20, pady=(0,10))
        ctk.CTkLabel(row1, text=f"This Month: {portions_this_month}", text_color="#374151", font=("Arial", 14)).pack(side="left")
        ctk.CTkLabel(row1, text=f"Avg Monthly: {avg_monthly_portions:.1f}", text_color="#374151", font=("Arial", 14)).pack(side="left", padx=25)
        ctk.CTkLabel(row1, text=f"Total: {total_portions}", text_color="#374151", font=("Arial", 14)).pack(side="left", padx=25)

        # Waste Reduction Report (From File 1 - Keep this feature)
        try:
            from src.model.laporandonasi import LaporanDonasi
            provider_reqs = RequestController.getRequestByProviderId(user.id)
            completed_reqs_for_report = [r for r in provider_reqs if r.status in ["Completed", "FeedbackSent"]]
            total_est = 0.0
            report_items = []
            for r in completed_reqs_for_report[:5]:
                lap = LaporanDonasi(idLaporan=0, idRequest=r.idRequest, tanggalLaporan="", jenisLaporan="Donasi", deskripsi="")
                est = lap.generateEstimasiPengurangan()
                total_est += est
                report_items.append((r.idRequest, est))

            report = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=10)
            report.pack(fill="x", pady=10)
            ctk.CTkLabel(report, text="Environmental Impact", font=("Arial", 18, "bold"), text_color="#132A13").pack(anchor="w", padx=20, pady=(15, 5))
            ctk.CTkLabel(report, text=f"Estimated waste reduction: {total_est:.2f} kg", text_color="#374151").pack(anchor="w", padx=20)
            
            list_frame = ctk.CTkFrame(report, fg_color="transparent")
            list_frame.pack(fill="x", padx=20, pady=10)
            for rid, est in report_items:
                row = ctk.CTkFrame(list_frame, fg_color="transparent")
                row.pack(fill="x", pady=2)
                ctk.CTkLabel(row, text=f"Request #{rid}", width=200, anchor="w").pack(side="left")
                ctk.CTkLabel(row, text=f"Est. Reduction {est:.2f} kg", anchor="w").pack(side="left")
        except Exception:
            pass


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

    def render_food_stock(self):
        header_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(header_frame, text="Available Food Items", font=("Arial", 20, "bold"), text_color="#132A13").pack(side="left")
        
        if getattr(self.app.current_user, "status", "aktif") == "banned":
            ctk.CTkLabel(header_frame, text="Account banned: actions disabled", text_color="#A16207").pack(side="right")
        else:
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
        except Exception:
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
        
        widths = [200, 130, 90, 110, 180] 

        ctk.CTkLabel(row, text=item.jenisMakanan, font=("Arial", 13), width=widths[0], anchor="w", text_color="#333").pack(side="left", padx=10)
        ctk.CTkLabel(row, text=item.batasWaktu, font=("Arial", 13), width=widths[1], anchor="w", text_color="#333").pack(side="left", padx=10)
        ctk.CTkLabel(row, text=str(item.jumlahPorsi), font=("Arial", 13), width=widths[2], anchor="w", text_color="#333").pack(side="left", padx=10)
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

        action_frame = ctk.CTkFrame(row, fg_color="transparent", width=widths[4])
        action_frame.pack(side="left", fill="x", padx=10)
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
        AddDonasiPopup(self.app.master, self.app, self.refresh_content)

    def popup_edit_donasi(self, item_to_edit):
        AddDonasiPopup(self.app.master, self.app, self.refresh_content, item_to_edit=item_to_edit)
        
    def hapus_donasi(self, idDonasi):
        if messagebox.askyesno("Confirm", "Delete this item?"):
            result = DonasiController.batalkanDonasi(idDonasi)
            if result and result.get("status") == "SUCCESS":
                messagebox.showinfo("Success", result.get("message", "Donation cancelled successfully."))
            else:
                messagebox.showerror("Error", result.get("message", "Failed to cancel donation."))
            self.refresh_content()


    def set_request_filter(self, status):
        self.request_filter = status
        self.refresh_content()

    def handle_request_action(self, request_id: int, action: str):
        if action == "Accept":
            new_status = "Preparing"
        elif action == "Reject":
            new_status = "Rejected"
        elif action == "Ready for Delivery":
            new_status = "On Delivery"
        elif action == "Completed":
            new_status = "Completed"
        else:
            messagebox.showerror("Error", "Aksi tidak dikenal.")
            return

        result = RequestController.updateStatus(request_id, new_status)
        
        if result["status"] == "SUCCESS":
            messagebox.showinfo("Success", result["message"])
            self.refresh_content()
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
                req for req in all_requests_by_provider if req.status == self.request_filter or (self.request_filter == "Completed" and req.status in ["Completed", "FeedbackSent"]) 
            ]
        def _to_dt(d):
            from datetime import datetime
            if hasattr(d, "strftime"):
                return d
            try:
                return datetime.fromisoformat(str(d))
            except Exception:
                return datetime.min
        filtered_requests = sorted(filtered_requests, key=lambda r: _to_dt(r.tanggalRequest), reverse=True)

        if not filtered_requests:
              ctk.CTkLabel(table_frame, text="Tidak ada permintaan makanan untuk saat ini.", font=("Arial", 14), text_color="gray").pack(pady=20)
        else:
            for req in filtered_requests:
                self.create_request_row(table_frame, req)

    def create_request_row(self, parent, req: RequestDonasi):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=5)
        
        widths = [70, 180, 120, 100, 100, 180] 

        ctk.CTkLabel(row, text=f"REQ{req.idRequest}", width=widths[0], anchor="w", text_color="#333").pack(side="left", padx=10)
        food_name = RequestController.getDonasiName(req.idDonasi)
        ctk.CTkLabel(row, text=food_name, width=widths[1], anchor="w", text_color="#333").pack(side="left", padx=10)
        receiver_name = RequestController.getReceiverName(req.idReceiver)
        ctk.CTkLabel(row, text=receiver_name, width=widths[2], anchor="w", text_color="#333").pack(side="left", padx=10)
        dval = req.tanggalRequest
        dtext = dval.strftime("%Y-%m-%d") if isinstance(dval, (datetime, date)) else str(dval)[:10]
        ctk.CTkLabel(row, text=dtext, width=widths[3], anchor="w", text_color="#333").pack(side="left", padx=10)

        # Status Badge
        status_colors = { 
            "Pending": ("#FEF9C3", "#A16207"), 
            "Preparing": ("#E0F2FE", "#075985"), 
            "On Delivery": ("#DBEAFE", "#1E40AF"), 
            "Completed": ("#DCFCE7", "#166534"), 
            "FeedbackSent": ("#DCFCE7", "#166534"), 
            "Rejected": ("#FEE2E2", "#B91C1C"), 
        }
        s_color, s_text = status_colors.get(req.status, ("#F3F4F6", "#6B7280"))
        
        ctk.CTkLabel(row, text=req.status, fg_color=s_color, text_color=s_text, corner_radius=15, width=90).pack(side="left", padx=10)

        action_frame = ctk.CTkFrame(row, fg_color="transparent", width=widths[5])
        action_frame.pack(side="left", fill="x", padx=10)

        if getattr(self.app.current_user, "status", "aktif") == "banned":
            ctk.CTkLabel(action_frame, text="Account banned", text_color="gray").pack(side="left", padx=2)
        elif req.status == "Pending":
            ctk.CTkButton(action_frame, text="Accept", width=70, fg_color="#10B981", hover_color="#059669", text_color="white", cursor="hand2", command=lambda: self.handle_request_action(req.idRequest, "Accept")).pack(side="left", padx=2)
            ctk.CTkButton(action_frame, text="Reject", width=70, fg_color="white", border_width=1, border_color="red", text_color="red", hover_color="#FEF2F2", cursor="hand2", command=lambda: self.handle_request_action(req.idRequest, "Reject")).pack(side="left", padx=2)
            
        elif req.status == "Preparing":
            ctk.CTkButton(action_frame, text="Ready for Delivery", width=150, fg_color="#4D70B9", hover_color="#4D70B9", text_color="white", cursor="hand2", command=lambda: self.handle_request_action(req.idRequest, "Ready for Delivery")).pack(side="left", padx=2)
            
        elif req.status == "On Delivery":
            ctk.CTkButton(action_frame, text="Done", width=80, fg_color="#10B981", hover_color="#059669", text_color="white", cursor="hand2", command=lambda: self.handle_request_action(req.idRequest, "Completed")).pack(side="left", padx=2)
            
        elif req.status in ["Completed", "FeedbackSent", "Rejected"]:
            ctk.CTkLabel(action_frame, text="No Action Needed", text_color="gray").pack(side="left", padx=2)
            
        ctk.CTkFrame(parent, height=1, fg_color="#EEE").pack(fill="x")


    def render_feedback(self):
        # 1. Update Header & enforce auto-ban check
        for widget in self.header_frame.winfo_children(): widget.destroy()
        try:
            from src.controller.feedback_controller import FeedbackController
            FeedbackController.check_and_ban_provider(self.app.current_user.id)
            from src.model.user import Pengguna
            self.app.current_user = Pengguna.find_by_id(self.app.current_user.id) or self.app.current_user
        except Exception:
            pass
        self.render_header("Feedback", "See what receivers think about your donations")

        # 2. Persiapan Data
        try:
            feedbacks = Feedback.by_provider(self.app.current_user.id)
        except AttributeError:
            feedbacks = []

        # Hitung rata-rata
        avg = FeedbackController.hitungRataRataProvider(self.app.current_user.id)
        total_feedback = len(feedbacks) if feedbacks else 0
        
        rounded = max(0, min(3, int(round(avg)))) if total_feedback > 0 else 0
        avg_text = f"{avg:.1f}" if total_feedback > 0 else "0.0"

        # --- 3. Summary Card ---
        summary_card = ctk.CTkFrame(self.content_frame, fg_color="white", corner_radius=16, border_width=2, border_color="#E5E7EB")
        summary_card.pack(fill="x", pady=(0, 25), ipadx=25, ipady=25)

        summary_content = ctk.CTkFrame(summary_card, fg_color="transparent")
        summary_content.pack(anchor="w")

        ctk.CTkLabel(summary_content, text=avg_text, font=("Arial", 48, "bold"), text_color="#F6A836").pack(side="left", padx=(0, 20))
        
        right_summary = ctk.CTkFrame(summary_content, fg_color="transparent")
        right_summary.pack(side="left", anchor="c")
        
        star_frame = ctk.CTkFrame(right_summary, fg_color="transparent")
        star_frame.pack(anchor="w", pady=(5,0))
        
        stars_full = "★" * rounded
        stars_empty = "☆" * (3 - rounded)
        
        ctk.CTkLabel(star_frame, text=stars_full, font=("Arial", 24), text_color="#F6A836", pady=0).pack(side="left")
        if stars_empty:
             ctk.CTkLabel(star_frame, text=stars_empty, font=("Arial", 24), text_color="#D1D5DB", pady=0).pack(side="left")

        ctk.CTkLabel(right_summary, text=f"Based on {total_feedback} feedback(s)", font=("Arial", 14), text_color="#6B7280").pack(anchor="w")

        # --- 4. Daftar List Feedback ---
        scroll = ctk.CTkScrollableFrame(self.content_frame, fg_color="transparent", label_anchor="w")
        scroll.pack(fill="both", expand=True)

        if not feedbacks:
            empty_state = ctk.CTkFrame(scroll, fg_color="transparent")
            empty_state.pack(pady=40, fill="x")
            ctk.CTkLabel(empty_state, text="No feedback received yet.", font=("Arial", 16, "bold"), text_color="#374151").pack()
            ctk.CTkLabel(empty_state, text="Wait for receivers to rate your donations.", font=("Arial", 14), text_color="#6B7280").pack()
            return

        for fb in feedbacks:
            card = ctk.CTkFrame(scroll, fg_color="white", corner_radius=16, border_width=2, border_color="#E5E7EB")
            card.pack(fill="x", pady=10, ipadx=20, ipady=20)

            header_row = ctk.CTkFrame(card, fg_color="transparent")
            header_row.pack(fill="x", pady=(0, 10))

            try:
                from src.model.user import Pengguna
                r = Pengguna.find_by_id(fb.idReceiver)
                receiver_display = r.nama if r else f"Receiver #{fb.idReceiver}"
            except Exception:
                receiver_display = f"Receiver #{fb.idReceiver}"
            ctk.CTkLabel(header_row, text=receiver_display, font=("Arial", 16, "bold"), text_color="#111827").pack(side="left", anchor="w")

            fb_rating = int(fb.rating)
            ind_stars_full = "★" * fb_rating
            ind_stars_empty = "☆" * (3 - fb_rating)
            
            star_container = ctk.CTkFrame(header_row, fg_color="transparent")
            star_container.pack(side="right")
            ctk.CTkLabel(star_container, text=ind_stars_full, font=("Arial", 18), text_color="#F6A836").pack(side="left")
            if ind_stars_empty:
                 ctk.CTkLabel(star_container, text=ind_stars_empty, font=("Arial", 18), text_color="#D1D5DB").pack(side="left")

            comment_text = fb.komentar if fb.komentar else "No comment provided."
            ctk.CTkLabel(card, text=comment_text, font=("Arial", 14), text_color="#374151", 
                         anchor="w", justify="left", wraplength=700).pack(fill="x")

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

        if str(user.status).lower() == "banned":
            alert = ctk.CTkFrame(card, fg_color="#FEF9C3", corner_radius=10)
            alert.pack(fill="x", padx=30, pady=(20, 0))
            ctk.CTkLabel(alert, text="Your account is banned due to low ratings.", text_color="#A16207").pack(anchor="w", padx=15, pady=10)

    def save_profile(self):
        user = self.app.current_user
        
        # Get values
        new_name = self.entry_name.get().strip()
        new_phone = self.entry_phone.get().strip()
        new_email = self.entry_email.get().strip()
        new_pass = self.entry_new_pass.get().strip()
        
        # Validate
        if not all([new_name, new_phone, new_email]):
            messagebox.showerror("Error", "Name, phone, and email cannot be empty!")
            return
        
        # Update user object
        user.nama = new_name
        user.noTelepon = new_phone
        user.email = new_email
        
        # Handle password change
        if new_pass:
            import hashlib
            user.password_hash = hashlib.sha256(new_pass.encode()).hexdigest()
        
        # Try to save
        try:
            user.update()
            messagebox.showinfo("Success", "Profile updated successfully!")
            self.refresh_content()
        except Exception as e:
            error_msg = str(e)
            if "Can't connect" in error_msg or "MySQL" in error_msg:
                messagebox.showerror("Database Error", "Cannot connect to database. Please check if MySQL server is running.")
            else:
                messagebox.showerror("Error", f"Failed to update profile: {error_msg}")

    pass

    def create_table_header(self, parent, headers):
        header_frame = ctk.CTkFrame(parent, fg_color="#F9FAFB", height=40)
        header_frame.pack(fill="x")
        
        if len(headers) == 6: 
            widths = [70, 180, 120, 100, 100, 180] 
        elif len(headers) == 5:
            widths = [200, 130, 90, 110, 180] 
        else:
            widths = [150] * len(headers) 

        for i, h in enumerate(headers):
            ctk.CTkLabel(header_frame, text=h, font=("Arial", 12, "bold"), 
                         width=widths[i], anchor="w", text_color="#666").pack(side="left", padx=10)
            
        ctk.CTkFrame(parent, height=1, fg_color="#DDD").pack(fill="x")

# =========================================================================
# CLASS AddDonasiPopup (Using File 1 version for Dropdown Location)
# =========================================================================
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

        # Using ComboBox from File 1 (Better UX)
        ctk.CTkLabel(content, text="Pickup Location (Address)", font=("Arial", 12, "bold"), text_color="#333").pack(anchor="w", pady=(5, 0))
        self.entry_lokasi = ctk.CTkComboBox(content, values=BANDUNG_LOCATIONS, width=450, state="readonly")
        self.entry_lokasi.pack(anchor="w", pady=(0, 10))
        
        ctk.CTkLabel(content, text="Expiration Date (YYYY-MM-DD)", font=("Arial", 12, "bold"), text_color="#333").pack(anchor="w", pady=(5, 0))
        date_row = ctk.CTkFrame(content, fg_color="transparent")
        date_row.pack(anchor="w", pady=(0, 20))
        self.entry_batas = ctk.CTkEntry(date_row, width=380, placeholder_text=date.today().strftime("%Y-%m-%d"))
        self.entry_batas.pack(side="left")
        ctk.CTkButton(date_row, text="Pick", width=60, fg_color="#F6A836", hover_color="#E59930", text_color="white", command=self.open_date_picker).pack(side="left", padx=10)
        
        if self.mode == "edit":
            self.entry_jenis.insert(0, self.item_to_edit.jenisMakanan)
            self.entry_porsi.insert(0, str(self.item_to_edit.jumlahPorsi) if self.item_to_edit.jumlahPorsi is not None else "")
            self.entry_lokasi.set(self.item_to_edit.lokasi)
            self.entry_batas.insert(0, self.item_to_edit.batasWaktu)
        
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkButton(btn_frame, text="Cancel", fg_color="white", border_width=1, border_color="#333", text_color="#333", hover_color="#F0F0F0", width=100, command=self.destroy).pack(side="right", padx=10)
        
        button_text = "Update Stock" if self.mode == "edit" else "Save Stock"
        ctk.CTkButton(btn_frame, text=button_text, fg_color="#F6A836", hover_color="#E59930", 
                      text_color="white", width=100, command=self.save_or_update_donasi).pack(side="right")

    def open_date_picker(self):
        self.dp_year = datetime.now().year
        self.dp_month = datetime.now().month
        self.dp = ctk.CTkToplevel(self)
        self.dp.title("Select Date")
        self.dp.resizable(False, False)
        self.dp.transient(self)
        self.dp.grab_set()
        try:
            self.dp.focus_force()
        except Exception:
            pass
        wrap = ctk.CTkFrame(self.dp, fg_color="#FFFFFF")
        wrap.pack(padx=15, pady=15)
        head = ctk.CTkFrame(wrap, fg_color="transparent")
        head.pack(fill="x")
        ctk.CTkButton(head, text="<", width=30, command=lambda: self.shift_month(-1)).pack(side="left")
        self.dp_label = ctk.CTkLabel(head, text=self.month_label(), font=("Arial", 14, "bold"))
        self.dp_label.pack(side="left", padx=10)
        ctk.CTkButton(head, text=">", width=30, command=lambda: self.shift_month(1)).pack(side="left")
        self.grid_frame = ctk.CTkFrame(wrap, fg_color="transparent")
        self.grid_frame.pack(pady=10)
        foot = ctk.CTkFrame(wrap, fg_color="transparent")
        foot.pack(fill="x")
        ctk.CTkButton(foot, text="Today", width=80, command=self.pick_today).pack(side="left")
        self.render_calendar()

    def month_label(self):
        return f"{calendar.month_name[self.dp_month]} {self.dp_year}"

    def shift_month(self, delta):
        m = self.dp_month + delta
        y = self.dp_year
        if m < 1:
            m = 12
            y -= 1
        elif m > 12:
            m = 1
            y += 1
        self.dp_month = m
        self.dp_year = y
        self.dp_label.configure(text=self.month_label())
        self.render_calendar()

    def render_calendar(self):
        for w in self.grid_frame.winfo_children():
            w.destroy()
        days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        for i, d in enumerate(days):
            ctk.CTkLabel(self.grid_frame, text=d, width=50).grid(row=0, column=i, padx=2, pady=2)
        weeks = calendar.monthcalendar(self.dp_year, self.dp_month)
        for r, week in enumerate(weeks, start=1):
            for c, day in enumerate(week):
                txt = "" if day == 0 else str(day)
                btn = ctk.CTkButton(self.grid_frame, text=txt or " ", width=50, cursor="hand2", command=lambda d=day: self.pick_day(d))
                btn.grid(row=r, column=c, padx=2, pady=2)

    def pick_day(self, day):
        if day == 0:
            return
        val = f"{self.dp_year}-{self.dp_month:02d}-{day:02d}"
        self.entry_batas.delete(0, 'end')
        self.entry_batas.insert(0, val)
        self.dp.destroy()

    def pick_today(self):
        t = datetime.now().strftime("%Y-%m-%d")
        self.entry_batas.delete(0, 'end')
        self.entry_batas.insert(0, t)
        self.dp.destroy()
        
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