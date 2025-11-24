import tkinter as tk
import customtkinter as ctk
import os

# Import halaman-halaman
from src.output.login_page import LoginPage
from src.output.register_page import RegisterPage
from src.output.provider_dashboard import ProviderDashboard
from src.output.receiver_dashboard import ReceiverDashboard
from src.output.admin_dashboard import AdminDashboard

# --- KONFIGURASI HD & TEMA ---
ctk.set_appearance_mode("Light")        # Mode Terang (Sesuai desain hijau/putih Anda)
ctk.set_default_color_theme("green")    # Tema warna default

class MainApp(ctk.CTk):  # Ubah dari tk.Tk menjadi ctk.CTk
    def __init__(self):
        super().__init__()
        
        self.title("FoodShare")
        self.geometry("1280x800")  # Ukuran awal yang lebih besar
        
        # Izinkan Fullscreen/Maximize
        self.resizable(True, True) 

        # Opsional: Mulai dalam keadaan Maximized (Windows)
        # self.after(0, lambda: self.state('zoomed'))

        self.current_user = None

        # --- CONTAINER SETUP ---
        # Menggunakan ctk.CTkFrame sebagai container utama
        container = ctk.CTkFrame(self, fg_color="transparent") 
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

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
            # Parent dikirim ke class halaman
            frame = PageClass(parent=container, app=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name: str):
        if page_name in self.frames:
            frame = self.frames[page_name]
            frame.tkraise()
            
            # Refresh dashboard data jika method tersedia
            if hasattr(frame, "show_dashboard"):
                try:
                    frame.show_dashboard()
                except Exception as e:
                    print(f"Error refreshing dashboard: {e}")
        else:
            print(f"Error: Page {page_name} not found.")

    def login_success(self, user):
        self.current_user = user
        print(f"Login berhasil sebagai: {user.role}")

        if user.role == "provider":
            self.show_frame("ProviderDashboard")
        elif user.role == "receiver":
            self.show_frame("ReceiverDashboard")
        elif user.role == "admin":
            self.show_frame("AdminDashboard")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()