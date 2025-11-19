import tkinter as tk
import customtkinter as ctk  # Disarankan import ini jika menggunakan komponen CTk

# Import halaman-halaman (Sesuaikan path import dengan struktur folder Anda)
# Saya menggunakan try-except agar kode ini aman dijalankan meski file lain belum ada
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

        # --- CONTAINER SETUP ---
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        # === PERBAIKAN PENTING DI SINI ===
        # Memberikan bobot 1 pada baris dan kolom container.
        # Ini memaksa elemen di dalamnya (LoginPage) untuk melar (stretch)
        # memenuhi seluruh area container, menghilangkan area abu-abu kosong.
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Daftar halaman yang akan dimuat
        pages = (
            LoginPage,
            RegisterPage,
            ProviderDashboard,
            ReceiverDashboard,
            AdminDashboard,
        )

        for PageClass in pages:
            page_name = PageClass.__name__
            # Membuat instance halaman
            frame = PageClass(parent=container, app=self)
            self.frames[page_name] = frame
            
            # sticky="nsew" akan bekerja karena parent (container) 
            # sudah memiliki rowconfigure/columnconfigure weight=1
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name: str):
        if page_name in self.frames:
            frame = self.frames[page_name]
            frame.tkraise()
            
            # Refresh dashboard jika method tersedia
            if hasattr(frame, "show_dashboard"):
                try:
                    frame.show_dashboard()
                except Exception:
                    pass
        else:
            print(f"Error: Page {page_name} not found.")

    def login_success(self, user):
        self.current_user = user
        print(f"Login berhasil sebagai: {user.role}") # Debugging

        if user.role == "provider":
            self.show_frame("ProviderDashboard")
        elif user.role == "receiver":
            self.show_frame("ReceiverDashboard")
        elif user.role == "admin":
            self.show_frame("AdminDashboard")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()