# src/view/main_app.py
import tkinter as tk

from src.output.login_page import LoginPage
from src.output.register_page import RegisterPage
from src.output.provider_dashboard import ProviderDashboard
from src.output.receiver_dashboard import ReceiverDashboard
from src.output.admin_dashboard import AdminDashboard

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Food Donation App")
        self.geometry("1200x720")
        self.configure(bg="#F0F0F0")
        self.resizable(False, False)

        self.current_user = None

        # Container
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}

        pages = (
            LoginPage,
            RegisterPage,
            ProviderDashboard,
            ReceiverDashboard,
            AdminDashboard,
        )

        for PageClass in pages:
            page_name = PageClass.__name__
            frame = PageClass(parent=container, app=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name: str):
        frame = self.frames[page_name]
        frame.tkraise()

    def login_success(self, user):
        self.current_user = user

        if user.role == "provider":
            self.show_frame("ProviderDashboard")
        elif user.role == "receiver":
            self.show_frame("ReceiverDashboard")
        elif user.role == "admin":
            self.show_frame("AdminDashboard")
