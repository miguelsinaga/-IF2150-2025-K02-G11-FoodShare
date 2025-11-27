import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
import re

from src.frontend.side_menu import SideMenu
from src.model.user import Pengguna
from src.model.makanan import DataMakanan
from src.model.reqdonasi import RequestDonasi

class AdminDashboard(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="#F6F6F6")
        self.app = app
        self.current_menu = "Dashboard"

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = None
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    def show_dashboard(self):
        self.render_ui()

    def render_ui(self):
        try:
            if str(getattr(self.app.current_user, "status", "")).lower() == "banned":
                from tkinter import messagebox
                messagebox.showerror("Akun Diblokir", "Akun Anda diblokir dan tidak dapat menggunakan dashboard.")
                self.app.current_user = None
                self.app.show_frame("LoginPage")
                return
        except Exception:
            pass
        if self.sidebar: self.sidebar.destroy()
        self.sidebar = SideMenu(
            self, self.app,
            menu_items=[
                ("Dashboard", lambda: self.switch("Dashboard")),
                ("Manage Users", lambda: self.switch("Manage Users")),
                ("Manage Donations", lambda: self.switch("Manage Donations")),
            ],
            active_item=self.current_menu
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        for w in self.content.winfo_children(): w.destroy()

        if self.current_menu == "Dashboard":
            self.render_overview()
        elif self.current_menu == "Manage Users":
            self.render_users()
        elif self.current_menu == "Manage Donations":
            self.render_donations()
        

    def switch(self, menu):
        self.current_menu = menu
        self.render_ui()

    # =========================
    # 1. Overview
    # =========================
    def render_overview(self):
        ctk.CTkLabel(self.content, text="Admin Dashboard", font=("Arial", 24, "bold"), text_color="#132A13").pack(anchor="w")
        ctk.CTkLabel(self.content, text="System overview and statistics.", text_color="gray").pack(anchor="w", pady=(0, 20))

        stats = ctk.CTkFrame(self.content, fg_color="transparent")
        stats.pack(fill="x", pady=10)

        total_users = len(Pengguna.all())
        total_donations = len(DataMakanan.all())
        total_requests = len(RequestDonasi.all())

        self.card(stats, "Total Users", str(total_users), "#132A13").pack(side="left", expand=True, fill="x", padx=5)
        self.card(stats, "Total Donations", str(total_donations), "#132A13").pack(side="left", expand=True, fill="x", padx=5)
        self.card(stats, "Total Requests", str(total_requests), "#132A13").pack(side="left", expand=True, fill="x", padx=5)

    def card(self, parent, title, val, bg_color):
        f = ctk.CTkFrame(parent, fg_color=bg_color, corner_radius=10)
        icon_bg = ctk.CTkFrame(f, width=40, height=40, corner_radius=20, fg_color="white")
        icon_bg.pack(anchor="w", padx=15, pady=(15, 5))
        ctk.CTkLabel(icon_bg, text="i", text_color=bg_color, font=("Arial", 16, "bold")).place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(f, text=title, text_color="#A0B0A0", font=("Arial", 12)).pack(anchor="w", padx=15)
        ctk.CTkLabel(f, text=val, font=("Arial", 28, "bold"), text_color="white").pack(anchor="w", padx=15, pady=(0, 15))
        return f

    # =========================
    # 2. Manage Users
    # =========================
    def render_users(self):
        ctk.CTkLabel(self.content, text="Manage Users", font=("Arial", 24, "bold"), text_color="#132A13").pack(anchor="w", pady=(0, 20))

        headers = ["ID", "Name", "Email", "Role", "Status", "Action"]
        widths = [60, 200, 300, 120, 120, 200]
        self.create_table_header(self.content, headers, widths)

        scroll = ctk.CTkScrollableFrame(self.content, fg_color="white", corner_radius=10)
        scroll.pack(fill="both", expand=True)

        users = Pengguna.all()
        for u in users:
            self.create_user_row(scroll, u, widths)

    def create_user_row(self, parent, user, widths):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=5)

        ctk.CTkLabel(row, text=str(user.id), width=widths[0], anchor="w", text_color="#333").pack(side="left", padx=10)
        ctk.CTkLabel(row, text=user.nama, width=widths[1], anchor="w", text_color="#333").pack(side="left", padx=10)
        ctk.CTkLabel(row, text=user.email, width=widths[2], anchor="w", text_color="#333").pack(side="left", padx=10)
        ctk.CTkLabel(row, text=user.role, width=widths[3], anchor="w", text_color="#333").pack(side="left", padx=10)

        # Tampilkan status untuk provider berdasarkan Donatur.status_akun
        status_disp = user.status
        status_color = "#E6F4EA"
        status_text_color = "#1E8E3E"
        if user.role == "provider":
            try:
                from src.backend.donatur_data import DonaturRepo
                d = DonaturRepo().find_by_user_id(user.id)
                if d and str(d.get("status_akun", "aktif")).lower() != "aktif":
                    status_disp = "banned"
                    status_color = "#FCE8E6"
                    status_text_color = "#D93025"
                else:
                    status_disp = "aktif"
                    status_color = "#E6F4EA"
                    status_text_color = "#1E8E3E"
            except Exception:
                pass
        else:
            if user.status != "aktif":
                status_color = "#FCE8E6"
                status_text_color = "#D93025"
        status_wrap = ctk.CTkFrame(row, fg_color=status_color, corner_radius=14, width=100, height=28)
        status_wrap.pack(side="left", padx=10)
        label_badge = ctk.CTkLabel(status_wrap, text=f"● {status_disp}", text_color=status_text_color, font=("Arial", 12))
        label_badge.place(relx=0.5, rely=0.5, anchor="center")

        action_frame = ctk.CTkFrame(row, fg_color="transparent", width=widths[5])
        action_frame.pack(side="left", fill="x", padx=10)
        ctk.CTkButton(action_frame, text="Edit", width=70, fg_color="#F6A836", hover_color="#E59930", text_color="white",
                      command=lambda: self.popup_edit_user(user)).pack(side="left", padx=5)

        if user.role == "admin":
            ctk.CTkLabel(action_frame, text="Admin protected", text_color="gray").pack(side="left", padx=5)
        else:
            btn_text = "Ban" if status_disp == "aktif" else "Active"
            btn_col = "#EF4444" if status_disp == "aktif" else "#10B981"
            ctk.CTkButton(action_frame, text=btn_text, width=70, fg_color=btn_col, hover_color=btn_col, text_color="white",
                          command=lambda: self.toggle_user_status(user)).pack(side="left", padx=5)

        ctk.CTkFrame(parent, height=1, fg_color="#EEE").pack(fill="x")

    def toggle_user_status(self, user):
        # Admin tidak dapat diban
        if user.role == "admin":
            messagebox.showinfo("Protected", "Admin tidak dapat diban.")
            return
        # Untuk provider: ubah status di DonaturRepo saja
        if user.role == "provider":
            from src.backend.donatur_data import DonaturRepo
            repo = DonaturRepo()
            d = repo.find_by_user_id(user.id)
            current = str((d or {}).get("status_akun", "aktif")).lower()
            new_status = "banned" if current == "aktif" else "aktif"
            if messagebox.askyesno("Confirm", f"Change status of {user.nama} to {new_status}?"):
                repo.update_status(user.id, new_status)
                messagebox.showinfo("Success", f"Provider status updated to {new_status}")
                self.render_ui()
            return
        # Non-provider: fallback ke users.status
        new_status = "banned" if user.status == "aktif" else "aktif"
        if messagebox.askyesno("Confirm", f"Change status of {user.nama} to {new_status}?"):
            user.status = new_status
            user.update()
            messagebox.showinfo("Success", f"User status updated to {new_status}")
            self.render_ui()

    def popup_edit_user(self, user):
        EditUserPopup(self, user, self.render_ui)

    # =========================
    # 3. Manage Donations
    # =========================
    def render_donations(self):
        ctk.CTkLabel(self.content, text="Manage Donations", font=("Arial", 24, "bold"), text_color="#132A13").pack(anchor="w", pady=(0, 20))

        headers = ["ID", "Provider ID", "Item", "Status", "Action"]
        widths = [60, 100, 350, 150, 200]
        self.create_table_header(self.content, headers, widths)

        scroll = ctk.CTkScrollableFrame(self.content, fg_color="white", corner_radius=10)
        scroll.pack(fill="both", expand=True)

        donations = DataMakanan.all()
        for d in donations:
            self.create_donation_row(scroll, d, widths)

    def create_donation_row(self, parent, donasi, widths):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=5)

        ctk.CTkLabel(row, text=str(donasi.idDonasi), width=widths[0], anchor="w", text_color="#333").pack(side="left", padx=10)
        ctk.CTkLabel(row, text=str(donasi.idProvider), width=widths[1], anchor="w", text_color="#333").pack(side="left", padx=10)
        ctk.CTkLabel(row, text=donasi.jenisMakanan, width=widths[2], anchor="w", text_color="#333").pack(side="left", padx=10)

        status_text = donasi.status
        if status_text == "Tersedia":
            s_bg, s_tc, disp = "#E6F4EA", "#1E8E3E", "Active"
        elif status_text in ["Dipesan", "Dikirim", "Preparing", "Diproses"]:
            s_bg, s_tc, disp = "#FEF9C3", "#A16207", status_text
        elif status_text in ["Dibatalkan", "Cancelled"]:
            s_bg, s_tc, disp = "#FCE8E6", "#D93025", status_text
        else:
            s_bg, s_tc, disp = "#E0F2FE", "#075985", status_text

        s_wrap = ctk.CTkFrame(row, fg_color=s_bg, corner_radius=14, width=120, height=28)
        s_wrap.pack(side="left", padx=10)
        label_badge = ctk.CTkLabel(s_wrap, text=f"● {disp}", text_color=s_tc, font=("Arial", 12))
        label_badge.place(relx=0.5, rely=0.5, anchor="center")

        action_frame = ctk.CTkFrame(row, fg_color="transparent", width=widths[4])
        action_frame.pack(side="left", fill="x", padx=10)
        ctk.CTkButton(action_frame, text="Edit", width=70, fg_color="#F6A836", hover_color="#E59930", text_color="white",
                      command=lambda: self.popup_edit_donation(donasi)).pack(side="left", padx=5)
        ctk.CTkButton(action_frame, text="Del", width=70, fg_color="#EF4444", hover_color="#B91C1C", text_color="white",
                      command=lambda: self.delete_donation(donasi)).pack(side="left", padx=5)

        ctk.CTkFrame(parent, height=1, fg_color="#EEE").pack(fill="x")

    def delete_donation(self, donasi):
        if messagebox.askyesno("Delete", f"Are you sure you want to cancel/delete donation #{donasi.idDonasi}?"):
            donasi.status = "Dibatalkan"
            donasi.update()
            messagebox.showinfo("Success", "Donation canceled")
            self.render_ui()

    def popup_edit_donation(self, donasi):
        EditDonationPopup(self, donasi, self.render_ui)

    # =========================
    # Helper: table header
    # =========================
    def create_table_header(self, parent, headers, widths):
        f = ctk.CTkFrame(parent, fg_color="#F9FAFB", height=40)
        f.pack(fill="x")
        for i, h in enumerate(headers):
            ctk.CTkLabel(f, text=h, font=("Arial", 12, "bold"), width=widths[i], anchor="w", text_color="#666").pack(side="left", padx=10)
        ctk.CTkFrame(parent, height=1, fg_color="#DDD").pack(fill="x")


# =========================
# Popup: Edit User
# =========================
class EditUserPopup(ctk.CTkToplevel):
    def __init__(self, parent, user, callback):
        super().__init__(parent)
        self.user = user
        self.callback = callback
        self.title("Edit User")
        self.geometry("400x450")
        self.transient(parent)
        self.grab_set()

        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(content, text="Full Name").pack(anchor="w")
        self.entry_nama = ctk.CTkEntry(content, width=300)
        self.entry_nama.insert(0, user.nama)
        self.entry_nama.pack(pady=(0, 10))

        ctk.CTkLabel(content, text="Email").pack(anchor="w")
        self.entry_email = ctk.CTkEntry(content, width=300)
        self.entry_email.insert(0, user.email)
        self.entry_email.pack(pady=(0, 10))

        ctk.CTkLabel(content, text="Phone").pack(anchor="w")
        self.entry_phone = ctk.CTkEntry(content, width=300)
        self.entry_phone.insert(0, user.noTelepon)
        self.entry_phone.pack(pady=(0, 10))

        ctk.CTkLabel(content, text="Role (provider/receiver/admin)").pack(anchor="w")
        self.entry_role = ctk.CTkEntry(content, width=300)
        self.entry_role.insert(0, user.role)
        self.entry_role.pack(pady=(0, 20))

        ctk.CTkButton(content, text="Save Changes", fg_color="#132A13", command=self.save).pack(fill="x")

    def save(self):
        nama = self.entry_nama.get().strip()
        email = self.entry_email.get().strip()
        phone = self.entry_phone.get().strip()
        role = self.entry_role.get().strip().lower()

        if not nama:
            messagebox.showerror("Error", "Nama tidak boleh kosong")
            return

        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            messagebox.showerror("Error", "Format email tidak valid")
            return

        existing = Pengguna.find_by_email(email)
        if existing and existing.id != self.user.id:
            messagebox.showerror("Error", "Email sudah digunakan oleh user lain")
            return

        if role not in {"provider", "receiver", "admin"}:
            messagebox.showerror("Error", "Role harus provider/receiver/admin")
            return

        if phone and not re.match(r"^\+?\d{6,15}$", phone):
            messagebox.showerror("Error", "No. telepon tidak valid")
            return

        self.user.nama = nama
        self.user.email = email
        self.user.noTelepon = phone
        self.user.role = role

        self.user.update()

        updated = Pengguna.find_by_id(self.user.id)
        if not updated or updated.email != email or updated.nama != nama or updated.noTelepon != phone or updated.role != role:
            messagebox.showerror("Error", "Gagal menyimpan perubahan ke database")
            return

        messagebox.showinfo("Success", "User updated successfully")
        self.callback()
        self.destroy()


# =========================
# Popup: Edit Donation
# =========================
class EditDonationPopup(ctk.CTkToplevel):
    def __init__(self, parent, donasi, callback):
        super().__init__(parent)
        self.donasi = donasi
        self.callback = callback
        self.title("Edit Donation")
        self.geometry("400x400")
        self.transient(parent)
        self.grab_set()

        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(content, text="Food Item").pack(anchor="w")
        self.entry_jenis = ctk.CTkEntry(content, width=300)
        self.entry_jenis.insert(0, donasi.jenisMakanan)
        self.entry_jenis.pack(pady=(0, 10))

        ctk.CTkLabel(content, text="Portions").pack(anchor="w")
        self.entry_porsi = ctk.CTkEntry(content, width=300)
        self.entry_porsi.insert(0, str(donasi.jumlahPorsi))
        self.entry_porsi.pack(pady=(0, 10))

        ctk.CTkLabel(content, text="Location").pack(anchor="w")
        self.entry_lokasi = ctk.CTkEntry(content, width=300)
        self.entry_lokasi.insert(0, donasi.lokasi)
        self.entry_lokasi.pack(pady=(0, 10))

        ctk.CTkButton(content, text="Save Changes", fg_color="#132A13", command=self.save).pack(fill="x", pady=20)

    def save(self):
        try:
            porsi = int(self.entry_porsi.get())
        except ValueError:
            messagebox.showerror("Error", "Portions must be a number")
            return

        self.donasi.jenisMakanan = self.entry_jenis.get()
        self.donasi.jumlahPorsi = porsi
        self.donasi.lokasi = self.entry_lokasi.get()

        self.donasi.update()
        messagebox.showinfo("Success", "Donation updated successfully")
        self.callback()
        self.destroy()
    def render_ban_audit(self):
        pass
    def recalc_ban(self, uid: int):
        pass
    def manual_unban(self, user):
        pass
