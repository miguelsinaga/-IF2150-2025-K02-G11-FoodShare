import customtkinter as ctk
from tkinter import ttk
import tkinter as tk

from src.frontend.side_menu import SideMenu
from src.model.user import Pengguna
from src.model.makanan import DataMakanan
from src.model.reqdonasi import RequestDonasi
from src.model.feedbackdonasi import Feedback

class AdminDashboard(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="#E5E7EB")
        self.app = app
        self.current_menu = "Dashboard"

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = None
        self.content = ctk.CTkFrame(self, fg_color="#F9FAFB")
        self.content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    def show_dashboard(self):
        self.render_ui()

    def render_ui(self):
        if self.sidebar: self.sidebar.destroy()
        self.sidebar = SideMenu(
            self, self.app,
            menu_items=[
                ("Dashboard", lambda: self.switch("Dashboard")),
                ("Users", lambda: self.switch("Users")),
                ("Donations", lambda: self.switch("Donations")),
            ],
            active_item=self.current_menu
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        for w in self.content.winfo_children(): w.destroy()

        if self.current_menu == "Dashboard":
            ctk.CTkLabel(self.content, text="Admin Dashboard", font=("Arial", 26, "bold"), text_color="#132A13").pack(pady=20)
            stats = ctk.CTkFrame(self.content, fg_color="transparent")
            stats.pack(fill="x")
            self.card(stats, "Total Users", str(len(Pengguna.all()))).pack(side="left", padx=10, expand=True, fill="x")
            self.card(stats, "Total Donations", str(len(DataMakanan.all()))).pack(side="left", padx=10, expand=True, fill="x")
        
        elif self.current_menu == "Users":
            ctk.CTkLabel(self.content, text="User List", font=("Arial", 24, "bold"), text_color="#132A13").pack(pady=20)
            self.create_treeview(["ID", "Name", "Email", "Role"])
            for u in Pengguna.all():
                self.tree.insert("", "end", values=(u.id, u.nama, u.email, u.role))

        elif self.current_menu == "Donations":
            ctk.CTkLabel(self.content, text="All Donations", font=("Arial", 24, "bold"), text_color="#132A13").pack(pady=20)
            self.create_treeview(["ID", "Provider", "Item", "Status"])
            for d in DataMakanan.all():
                self.tree.insert("", "end", values=(d.idDonasi, d.idProvider, d.jenisMakanan, d.status))

    def switch(self, menu):
        self.current_menu = menu
        self.render_ui()

    def card(self, parent, title, val):
        f = ctk.CTkFrame(parent, fg_color="white", height=100)
        ctk.CTkLabel(f, text=title, text_color="gray").pack(pady=(20, 5))
        ctk.CTkLabel(f, text=val, font=("Arial", 30, "bold"), text_color="#132A13").pack()
        return f

    def create_treeview(self, cols):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=30, font=("Arial", 11))
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
        
        self.tree = ttk.Treeview(self.content, columns=cols, show="headings", height=15)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=150)
        self.tree.pack(fill="both", expand=True)