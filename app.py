
import tkinter as tk
import customtkinter as ctk

# Import halaman-halaman
from src.frontend.login_page import LoginPage
from src.frontend.register_page import RegisterPage
from src.frontend.provider_dashboard import ProviderDashboard
from src.frontend.receiver_dashboard import ReceiverDashboard
from src.frontend.admin_dashboard import AdminDashboard
#from src.frontend.forgot_password import ForgotPassword
# --- KONFIGURASI HD & TEMA ---
ctk.set_appearance_mode("Light")        # Mode Terang (Sesuai desain hijau/putih Anda)
ctk.set_default_color_theme("green")    # Tema warna default
class MainApp(ctk.CTk):  # Ubah dari tk.Tk menjadi ctk.CTk
    def __init__(self):
        super().__init__()
        
        self.title("Food Donation App")
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
            #ForgotPassword,
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
        try:
            from tkinter import messagebox
        except Exception:
            pass
        # Jika akun banned → paksa logout dengan pesan
        if str(getattr(user, "status", "")).lower() == "banned":
            try:
                messagebox.showerror("Akun Diblokir", "Akun Anda diblokir dan tidak dapat login.")
            except Exception:
                pass
            self.current_user = None
            self.show_frame("LoginPage")
            return

        if user.role == "provider":
            try:
                from src.controller.feedback_controller import FeedbackController
                FeedbackController.check_and_ban_provider(user.id)
                from src.model.user import Pengguna
                updated = Pengguna.find_by_id(user.id)
                if updated:
                    self.current_user = updated
                if str(getattr(self.current_user, "status", "")).lower() == "banned":
                    try:
                        messagebox.showerror("Akun Diblokir", "Akun Anda diblokir dan tidak dapat login.")
                    except Exception:
                        pass
                    self.current_user = None
                    self.show_frame("LoginPage")
                    return
            except Exception:
                pass
            self.show_frame("ProviderDashboard")
        elif user.role == "receiver":
            self.show_frame("ReceiverDashboard")
        elif user.role == "admin":
            self.show_frame("AdminDashboard")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
