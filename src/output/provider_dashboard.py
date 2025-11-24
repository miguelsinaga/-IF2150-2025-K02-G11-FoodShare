import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from datetime import datetime, date 
from PIL import Image
import os 

from src.output.side_menu import SideMenu
from src.controller.donasi_controller import DonasiController
from src.controller.request_controller import RequestController
from src.model.feedbackdonasi import Feedback
from src.model.makanan import DataMakanan

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
        
        self.header_frame = ctk.CTkFrame(self.main_area, height=80, fg_color="white", corner_radius=0)
        self.header_frame.pack(side="top", fill="x")
        self.header_frame.pack_propagate(False) 

        self.content_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.content_frame.pack(side="top", fill="both", expand=True, padx=20, pady=20)

        self.load_icons()

    def load_icons(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.join(script_dir, "../../src/assets") 
        icon_names = {"Active Stocks": "active.png", "New Requests": "newrequest.png", "On Delivery": "delivery.png", "Total Donations": "completed.png"}
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
                ("Food Stock", lambda: self.switch_menu("Food Stock")),
                ("Food Requests", lambda: self.switch_menu("Food Requests")),
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

    # ============================================
    # HEADER (DIPERBAIKI: Hapus Notif & Rapatkan Teks)
    # ============================================
    def render_header(self, title, subtitle):
        left_c = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        left_c.pack(side="left", padx=30, pady=15)
        ctk.CTkLabel(left_c, text=title, font=("Arial", 24, "bold"), text_color="#132A13").pack(anchor="w")
        ctk.CTkLabel(left_c, text=subtitle, font=("Arial", 13), text_color="gray").pack(anchor="w")

        right_c = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        right_c.pack(side="right", padx=30)

        # -- HAPUS TOMBOL NOTIFIKASI DI SINI --
        # (Kode bell icon dihapus)

        user = self.app.current_user
        initials = user.nama[:2].upper() if user.nama else "??"
        
        avatar = ctk.CTkFrame(right_c, width=40, height=40, corner_radius=20, fg_color="#132A13")
        avatar.pack(side="left", padx=10)
        ctk.CTkLabel(avatar, text=initials, text_color="#C5E064", font=("Arial", 14, "bold")).place(relx=0.5, rely=0.5, anchor="center")

        info = ctk.CTkFrame(right_c, fg_color="transparent")
        info.pack(side="left")
        
        # -- PERBAIKAN JARAK TEKS: pady=0 --
        ctk.CTkLabel(info, text=user.nama, font=("Arial", 14, "bold"), text_color="#132A13").pack(anchor="w", pady=0)
        ctk.CTkLabel(info, text="Provider", font=("Arial", 11), text_color="gray").pack(anchor="w", pady=0)

    # ============================================
    # FOOD REQUESTS (DIPERBAIKI: Tinggi Baris & Tombol Done)
    # ============================================
    def render_food_requests(self):
        filter_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        filter_frame.pack(anchor="w", pady=(0, 10))
        for f in ["All", "Pending", "Preparing", "On Delivery", "Completed"]:
            fg = "#132A13" if f == self.request_filter else "white"
            tc = "white" if f == self.request_filter else "#132A13"
            ctk.CTkButton(filter_frame, text=f, fg_color=fg, text_color=tc, width=80, corner_radius=15, border_width=1, border_color="#DDD", command=lambda s=f: self.set_request_filter(s)).pack(side="left", padx=5)

        scroll = ctk.CTkScrollableFrame(self.content_frame, fg_color="white", corner_radius=10)
        scroll.pack(fill="both", expand=True)
        
        h_frame = ctk.CTkFrame(scroll, fg_color="#F9FAFB", height=40)
        h_frame.pack(fill="x")
        cols = ["Req ID", "Item", "Receiver", "Date", "Status", "Action"]
        widths = [70, 180, 120, 100, 100, 180]
        for i, c in enumerate(cols):
            ctk.CTkLabel(h_frame, text=c, font=("Arial",12,"bold"), width=widths[i], anchor="w", text_color="#666").pack(side="left", padx=5)

        all_req = RequestController.getRequestByProviderId(self.app.current_user.id)
        filtered = all_req if self.request_filter == "All" else [r for r in all_req if r.status == self.request_filter]
        
        if not filtered:
            ctk.CTkLabel(scroll, text="No requests found.", text_color="gray").pack(pady=20)
            return

        for req in filtered:
            self.create_request_row(scroll, req)

    def create_request_row(self, parent, req):
        # -- PERBAIKAN TINGGI BARIS: height=50, pack_propagate(False) --
        row = ctk.CTkFrame(parent, fg_color="transparent", height=50)
        row.pack(fill="x", pady=0) 
        row.pack_propagate(False) # Kunci: Mencegah baris mengecil/membesar
        
        widths = [70, 180, 120, 100, 100, 180]
        
        # Gunakan place untuk centering vertikal di dalam row fixed height
        # Atau gunakan pack dengan frame di dalamnya. Untuk mudahnya kita pakai pack side=left di dalam container.
        
        # Container internal agar mudah di-align vertical center (opsional), 
        # tapi dengan pack_propagate(False) di row, kita bisa langsung pack elemen.
        
        # Karena pack_propagate(False) mematikan auto-size, kita harus hati-hati.
        # Cara paling aman untuk list adalah frame biasa (tanpa fixed height) tapi pastikan ISI-nya konsisten.
        # MENGGANTI PENDEKATAN: Biarkan row auto-height, tapi pastikan Action Frame SELALU punya height.
        
        row.configure(height=0) # Reset manual height config if needed
        row.pack_propagate(True) # Re-enable propagate for auto fit, BUT force content size.
        
        # Req ID
        ctk.CTkLabel(row, text=f"#{req.idRequest}", width=widths[0], anchor="w").pack(side="left", padx=5, pady=10)
        
        # Food Name
        ctk.CTkLabel(row, text=RequestController.getDonasiName(req.idDonasi), width=widths[1], anchor="w").pack(side="left", padx=5, pady=10)
        
        # Receiver Name (Sudah diperbaiki di Controller)
        ctk.CTkLabel(row, text=RequestController.getReceiverName(req.idReceiver), width=widths[2], anchor="w").pack(side="left", padx=5, pady=10)
        
        # Date
        ctk.CTkLabel(row, text=req.tanggalRequest[:10], width=widths[3], anchor="w").pack(side="left", padx=5, pady=10)
        
        # Status Badge
        colors = {"Pending":("#FEF9C3","#A16207"), "Preparing":("#E0F2FE","#075985"), "On Delivery":("#DBEAFE","#1E40AF"), "Completed":("#DCFCE7","#166534"), "Rejected":("#FEE2E2","#B91C1C")}
        bg, tc = colors.get(req.status, ("#EEE","#333"))
        ctk.CTkLabel(row, text=req.status, fg_color=bg, text_color=tc, corner_radius=10, width=90).pack(side="left", padx=5, pady=10)
        
        # Action Frame (Fix Tinggi di sini)
        act = ctk.CTkFrame(row, fg_color="transparent", width=widths[5], height=40) # Fix width & height container action
        act.pack(side="left", padx=5, pady=5)
        act.pack_propagate(False) # Pastikan frame action tingginya tetap meski kosong
        
        if req.status == "Pending":
            ctk.CTkButton(act, text="✓", width=40, fg_color="#10B981", text_color="white", command=lambda: self.handle_request_action(req.idRequest, "Accept")).pack(side="left", padx=2, pady=5)
            ctk.CTkButton(act, text="X", width=40, fg_color="white", border_color="red", border_width=1, text_color="red", hover_color="#FEF2F2", command=lambda: self.handle_request_action(req.idRequest, "Reject")).pack(side="left", padx=2, pady=5)
        
        elif req.status == "Preparing":
            ctk.CTkButton(act, text="Send", width=80, fg_color="#4D70B9", text_color="white", command=lambda: self.handle_request_action(req.idRequest, "Ready for Delivery")).pack(side="left", pady=5)
        
        # -- PERBAIKAN LOGIC TOMBOL DONE --
        elif req.status == "On Delivery":
            ctk.CTkButton(act, text="Done", width=80, fg_color="#10B981", hover_color="#059669", text_color="white", command=lambda: self.handle_request_action(req.idRequest, "Completed")).pack(side="left", pady=5)
        
        ctk.CTkFrame(parent, height=1, fg_color="#EEE").pack(fill="x")

    def handle_request_action(self, rid, act):
        ns = ""
        if act == "Accept": ns = "Preparing"
        elif act == "Reject": ns = "Rejected"
        elif act == "Ready for Delivery": ns = "On Delivery"
        elif act == "Completed": ns = "Completed" # Logic baru
        else: return
        
        RequestController.updateStatus(rid, ns)
        self.refresh_content()

    # ============================================
    # FUNGSI LAIN (Sama seperti sebelumnya)
    # ============================================
    def render_overview(self):
        # ... (Kode render overview sama seperti sebelumnya)
        user = self.app.current_user
        stats = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        stats.pack(fill="x", pady=10)

        try: all_donasi = DonasiController.semuaDonasi()
        except: all_donasi = DonasiController.getDonasiAktif()
        my_donasi = [d for d in all_donasi if str(getattr(d, 'idProvider', 0)) == str(user.id)]
        my_ids = [d.idDonasi for d in my_donasi]
        all_req = RequestController.semuaRequest()
        my_req = [r for r in all_req if r.idDonasi in my_ids]

        active = sum(1 for d in my_donasi if d.status == "Tersedia")
        pending = sum(1 for r in my_req if r.status == "Pending")
        delivery = sum(1 for r in my_req if r.status == "On Delivery")
        completed = sum(1 for r in RequestController.getRequestByProviderId(user.id) if r.status == "Completed")

        self.create_stat_card(stats, "Active Stocks", str(active), "#132A13").pack(side="left", expand=True, fill="x", padx=5)
        self.create_stat_card(stats, "New Requests", str(pending), "#132A13").pack(side="left", expand=True, fill="x", padx=5)
        self.create_stat_card(stats, "On Delivery", str(delivery), "#132A13").pack(side="left", expand=True, fill="x", padx=5)
        self.create_stat_card(stats, "Total Donations", str(completed), "#132A13").pack(side="left", expand=True, fill="x", padx=5)

        banner = ctk.CTkFrame(self.content_frame, fg_color="#DCEE85", corner_radius=10)
        banner.pack(fill="x", pady=30, ipady=10)
        ctk.CTkLabel(banner, text="♻ You've helped share meals this month.", text_color="#132A13", font=("Arial", 16, "bold")).pack(anchor="w", padx=20)

    def create_stat_card(self, parent, title, value, bg_color):
        card = ctk.CTkFrame(parent, fg_color=bg_color, corner_radius=10)
        icon_bg = ctk.CTkFrame(card, width=40, height=40, corner_radius=20, fg_color="white")
        icon_bg.pack(anchor="w", padx=15, pady=(15, 5))
        img = self.icon_cache.get(title)
        if img: ctk.CTkLabel(icon_bg, text="", image=img).place(relx=0.5, rely=0.5, anchor="center")
        else: ctk.CTkLabel(icon_bg, text="?", text_color=bg_color).place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(card, text=title, font=("Arial", 12), text_color="#A0B0A0").pack(anchor="w", padx=15)
        ctk.CTkLabel(card, text=value, font=("Arial", 28, "bold"), text_color="white").pack(anchor="w", padx=15, pady=(0, 15))
        return card

    def render_food_stock(self):
        header_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        ctk.CTkButton(header_frame, text="+ Add Availability", fg_color="#F6A836", hover_color="#E59930", text_color="white", command=self.popup_add_donasi).pack(side="right")
        
        scroll = ctk.CTkScrollableFrame(self.content_frame, fg_color="white", corner_radius=10)
        scroll.pack(fill="both", expand=True)
        h_frame = ctk.CTkFrame(scroll, fg_color="#F9FAFB", height=40)
        h_frame.pack(fill="x")
        cols = ["Food Item", "Expiration", "Portions", "Status", "Action"]
        widths = [200, 130, 90, 110, 180]
        for i, c in enumerate(cols):
            ctk.CTkLabel(h_frame, text=c, font=("Arial",12,"bold"), width=widths[i], anchor="w", text_color="#666").pack(side="left", padx=5)
        self.render_stock_rows(scroll)

    def render_stock_rows(self, parent):
        try: all_d = DonasiController.semuaDonasi()
        except: all_d = DonasiController.getDonasiAktif()
        user_id = str(self.app.current_user.id)
        my_d = [d for d in all_d if str(getattr(d,'idProvider',0)) == user_id and d.status not in ["Completed","Cancelled"]]
        
        if not my_d:
            ctk.CTkLabel(parent, text="No stocks.", text_color="gray").pack(pady=20)
            return

        for item in my_d:
            row = ctk.CTkFrame(parent, fg_color="transparent")
            row.pack(fill="x", pady=5)
            widths = [200, 130, 90, 110, 180]
            ctk.CTkLabel(row, text=item.jenisMakanan, width=widths[0], anchor="w").pack(side="left", padx=5)
            ctk.CTkLabel(row, text=item.batasWaktu, width=widths[1], anchor="w").pack(side="left", padx=5)
            ctk.CTkLabel(row, text=str(item.jumlahPorsi), width=widths[2], anchor="w").pack(side="left", padx=5)
            st = item.status
            bg = "#E6F4EA" if st=="Tersedia" else "#FEF9C3"
            tc = "#1E8E3E" if st=="Tersedia" else "#A16207"
            ctk.CTkLabel(row, text=st, fg_color=bg, text_color=tc, corner_radius=10, width=90).pack(side="left", padx=5)
            act = ctk.CTkFrame(row, fg_color="transparent", width=widths[4])
            act.pack(side="left", padx=5)
            ctk.CTkButton(act, text="Edit", width=60, fg_color="white", border_color="#DDD", border_width=1, text_color="#333", hover_color="#F0F0F0", command=lambda x=item: self.popup_edit_donasi(x)).pack(side="left", padx=2)
            ctk.CTkButton(act, text="Del", width=60, fg_color="white", border_color="red", border_width=1, text_color="red", hover_color="#FEF2F2", command=lambda x=item: self.hapus_donasi(x.idDonasi)).pack(side="left", padx=2)
            ctk.CTkFrame(parent, height=1, fg_color="#EEE").pack(fill="x")

    def render_feedback(self):
        scroll = ctk.CTkScrollableFrame(self.content_frame, fg_color="transparent")
        scroll.pack(fill="both", expand=True)
        feedbacks = Feedback.by_provider(self.app.current_user.id)
        if not feedbacks:
            ctk.CTkLabel(scroll, text="No feedbacks yet.", text_color="gray").pack(pady=20)
            return
        for fb in feedbacks:
            card = ctk.CTkFrame(scroll, fg_color="white", corner_radius=10, border_width=1, border_color="#DDD")
            card.pack(fill="x", pady=5, ipadx=10, ipady=10)
            ctk.CTkLabel(card, text=f"From User #{fb.idReceiver}", font=("Arial",12,"bold")).pack(anchor="w")
            ctk.CTkLabel(card, text="★"*fb.rating, text_color="#F6A836").pack(anchor="w")
            ctk.CTkLabel(card, text=fb.komentar, text_color="#555").pack(anchor="w")

    def render_profile(self):
        # ... (Profile logic sama seperti sebelumnya)
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
        self.render_header("Profile", "Manage your profile settings here")

    def set_request_filter(self, s):
        self.request_filter = s
        self.refresh_content()

    def popup_add_donasi(self):
        AddDonasiPopup(self.app.master, self.app, self.refresh_content)

    def popup_edit_donasi(self, item):
        AddDonasiPopup(self.app.master, self.app, self.refresh_content, item_to_edit=item)

    def hapus_donasi(self, did):
        if messagebox.askyesno("Confirm", "Delete?"):
            DonasiController.batalkanDonasi(did)
            self.refresh_content()

class AddDonasiPopup(ctk.CTkToplevel):
    def __init__(self, parent, app_instance, refresh_callback, item_to_edit=None):
        super().__init__(parent)
        self.app = app_instance 
        self.refresh_callback = refresh_callback
        self.item_to_edit = item_to_edit
        self.title("Manage Stock")
        self.geometry("500x500")
        self.create_widgets()

    def create_widgets(self):
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(padx=20, pady=20, fill="both", expand=True)
        
        ctk.CTkLabel(content, text="Food Name").pack(anchor="w")
        self.entry_jenis = ctk.CTkEntry(content, width=400)
        self.entry_jenis.pack(pady=5)
        
        ctk.CTkLabel(content, text="Portions").pack(anchor="w")
        self.entry_porsi = ctk.CTkEntry(content, width=400)
        self.entry_porsi.pack(pady=5)
        
        ctk.CTkLabel(content, text="Location").pack(anchor="w")
        self.entry_lokasi = ctk.CTkEntry(content, width=400)
        self.entry_lokasi.pack(pady=5)
        
        ctk.CTkLabel(content, text="Expiry (YYYY-MM-DD)").pack(anchor="w")
        self.entry_batas = ctk.CTkEntry(content, width=400)
        self.entry_batas.pack(pady=5)
        
        if self.item_to_edit:
            self.entry_jenis.insert(0, self.item_to_edit.jenisMakanan)
            self.entry_porsi.insert(0, str(self.item_to_edit.jumlahPorsi))
            self.entry_lokasi.insert(0, self.item_to_edit.lokasi)
            self.entry_batas.insert(0, self.item_to_edit.batasWaktu)
            
        ctk.CTkButton(content, text="Save", fg_color="#132A13", command=self.save).pack(pady=20)

    def save(self):
        data = {
            "jenisMakanan": self.entry_jenis.get(),
            "jumlahPorsi": self.entry_porsi.get(),
            "lokasi": self.entry_lokasi.get(),
            "batasWaktu": self.entry_batas.get()
        }
        if self.item_to_edit:
            data["idDonasi"] = self.item_to_edit.idDonasi
            DonasiController.updateDonasi(data)
        else:
            DonasiController.buatDonasi(self.app.current_user.id, data)
        
        self.refresh_callback()
        self.destroy()