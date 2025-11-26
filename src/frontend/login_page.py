import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image
import os
from flask import Flask,request,jsonify
#from src.controller.account_controller_api import AkunControllerAPI as AccountController
# Fallback import controller
from src.backend.api.client_api import api_login

try:
    from src.controller.account_controller import AkunController
except ImportError:
    pass 

class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        # Set warna background utama menjadi Hijau Lime (#DCEE85)
        super().__init__(parent, fg_color="#DCEE85")
        self.app = app
        
        # FOR COLORS
        self.colors = {
            "bg_main": "#DCEE85",
            "card_bg": "#FFFFFF",
            "input_bg": "#132A13",
            "input_fg": "#FFFFFF",
            "placeholder": "#A0B0A0",
            "btn_bg": "#FFB03B",
            "btn_hover": "#E5A035",
            "text_header": "#132A13",
            "text_sub": "#556B2F",
            "dot_active": "#132A13",
            "dot_inactive": "#C5E064"
        }

        self.grid_columnconfigure(0, weight=1) 
        self.grid_columnconfigure(1, weight=1) 
        self.grid_rowconfigure(0, weight=1)

        # FOR CAROUSEL (IMAGE DI DIV KIRI)
        self.carousel_images = []
        self.carousel_index = 0
        self.is_animating = False
        self.auto_play_task = None

        # LEFT DIV
        self.left_card = ctk.CTkFrame(self, fg_color=self.colors["card_bg"], corner_radius=40)
        self.left_card.grid(row=0, column=0, sticky="nsew", padx=(30, 15), pady=30)
        
        self.logo_container = ctk.CTkFrame(self.left_card, fg_color="transparent")
        self.logo_container.place(relx=0.5, rely=0.2, anchor="center")

        image_path = "img/logo.png"
        if os.path.exists(image_path):
            pil_image = Image.open(image_path)
            self.logo_image = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(120, 120))
            ctk.CTkLabel(self.logo_container, text="", image=self.logo_image).pack(pady=(0, 5))
        else:
            ctk.CTkLabel(self.logo_container, text="[LOGO]", font=("Arial", 20)).pack(pady=(0, 5))


        ctk.CTkLabel(self.logo_container, text="FoodShare", 
                     font=("Arial", 28, "bold"), text_color="#E89D30").pack(pady=(0, 5))

        slogan_frame = ctk.CTkFrame(self.logo_container, fg_color="transparent")
        slogan_frame.pack()
        ctk.CTkLabel(slogan_frame, text="Share More, ", font=("Arial", 14, "bold"), text_color="#132A13").pack(side="left")
        ctk.CTkLabel(slogan_frame, text="Waste Less", font=("Arial", 14, "bold"), text_color="#A4C639").pack(side="left")

        self.carousel_container = ctk.CTkFrame(self.left_card, fg_color="transparent")
        self.carousel_container.place(relx=0.5, rely=0.65, anchor="center") 
        self.setup_carousel()

        # LOGIN FORM
        self.right_panel = ctk.CTkFrame(self, fg_color="transparent")
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=(15, 30), pady=30)

        self.form_container = ctk.CTkFrame(self.right_panel, fg_color="transparent", width=350)
        self.form_container.place(relx=0.5, rely=0.5, anchor="center")

        # 1. Header Text
        ctk.CTkLabel(self.form_container, text="Welcome Back!", 
                     font=("Arial", 28, "bold"), text_color=self.colors["text_header"]).pack(pady=(0, 5))
        
        ctk.CTkLabel(self.form_container, text="Login to your account", 
                     font=("Arial", 14), text_color=self.colors["text_sub"]).pack(pady=(0, 40))

        # 2. Input Username
        self.email_entry = ctk.CTkEntry(
            self.form_container, width=350, height=55, corner_radius=15,
            fg_color=self.colors["input_bg"], text_color=self.colors["input_fg"],
            placeholder_text="Username", placeholder_text_color=self.colors["placeholder"],
            border_width=0, font=("Arial", 14)
        )
        self.email_entry.pack(pady=(0, 20))

        # 3. Input Password
        self.password_entry = ctk.CTkEntry(
            self.form_container, width=350, height=55, corner_radius=15,
            fg_color=self.colors["input_bg"], text_color=self.colors["input_fg"],
            placeholder_text="Password", placeholder_text_color=self.colors["placeholder"],
            border_width=0, show="*", font=("Arial", 14)
        )
        self.password_entry.pack(pady=(0, 10))

        # 4. Forgot Password Link (Efek Hover Khusus)
        self.forgot_btn = ctk.CTkButton(
            self.form_container, text="Forgot Password?", font=("Arial", 12, "bold"),
            fg_color="transparent", text_color="#132A13", hover_color=self.colors["bg_main"],
            anchor="e", width=350, cursor="hand2", command=lambda: print("Forgot Password clicked")
        )
        # Bind events untuk ubah warna teks saat hover
        self.forgot_btn.bind("<Enter>", lambda e: self.forgot_btn.configure(text_color="#FFB03B"))
        self.forgot_btn.bind("<Leave>", lambda e: self.forgot_btn.configure(text_color="#132A13"))
        self.forgot_btn.pack(pady=(0, 25))

        # 5. Tombol Login
        self.login_btn = ctk.CTkButton(
            self.form_container, text="Login", font=("Arial", 18, "bold"),
            width=350, height=55, corner_radius=15, fg_color=self.colors["btn_bg"],
            text_color="#132A13", hover_color=self.colors["btn_hover"], cursor="hand2",
            command=self.do_login
        )
        self.login_btn.pack(pady=(0, 25))

        # 6. Sign Up Area (Efek Hover pada Teks "sign up")
        signup_frame = ctk.CTkFrame(self.form_container, fg_color="transparent")
        signup_frame.pack()

        ctk.CTkLabel(signup_frame, text="Don't have an account? ", font=("Arial", 12), text_color="#556B2F").pack(side="left")
        
        self.signup_btn = ctk.CTkButton(
            signup_frame, text="sign up", font=("Arial", 12, "bold"),
            fg_color="transparent", text_color="#132A13", width=50,
            hover_color=self.colors["bg_main"], cursor="hand2",
            command=lambda: app.show_frame("RegisterPage")
        )
        # Bind events manual untuk text color change
        self.signup_btn.bind("<Enter>", lambda e: self.signup_btn.configure(text_color="#FFB03B"))
        self.signup_btn.bind("<Leave>", lambda e: self.signup_btn.configure(text_color="#132A13"))
        self.signup_btn.pack(side="left")

    # LOGIC FOR CAROUSEL
    def setup_carousel(self):
        base = "img"
        files = [
            os.path.join(base, "PhotoCarousel1.jpg"),
            os.path.join(base, "PhotoCarousel2.jpg"),
            os.path.join(base, "PhotoCarousel3.jpg"),
            os.path.join(base, "PhotoCarousel4.jpg"),
        ]
        
        img_w, img_h = 500, 320 
        
        for f in files:
            try:
                pil = Image.open(f)
                self.carousel_images.append(ctk.CTkImage(light_image=pil, dark_image=pil, size=(img_w, img_h)))
            except Exception:
                pass
                
        if not self.carousel_images:
            lbl = ctk.CTkLabel(self.carousel_container, text="[Carousel Images Missing]", text_color="#132A13")
            lbl.pack()
            return
            
        self.carousel_index = 0
        
        self.carousel_container.configure(width=img_w, height=img_h + 50) 

        self.carousel_current = ctk.CTkLabel(self.carousel_container, text="", image=self.carousel_images[0])
        self.carousel_current.place(relx=0.5, rely=0.45, anchor="center")

        self.dots_frame = ctk.CTkFrame(self.carousel_container, fg_color="transparent")
        self.dots_frame.place(relx=0.5, rely=0.95, anchor="center")
        
        self.create_dots()
        self.start_auto_play()

    def create_dots(self):
        self.dots_widgets = []
        for i in range(len(self.carousel_images)):
            dot = ctk.CTkButton(
                self.dots_frame, 
                text="", 
                width=12, 
                height=12, 
                corner_radius=6,
                fg_color=self.colors["dot_active"] if i == 0 else self.colors["dot_inactive"],
                hover_color=self.colors["dot_active"],
                command=lambda idx=i: self.manual_slide(idx)
            )
            dot.pack(side="left", padx=5)
            self.dots_widgets.append(dot)

    def update_dots(self):
        for i, dot in enumerate(self.dots_widgets):
            color = self.colors["dot_active"] if i == self.carousel_index else self.colors["dot_inactive"]
            dot.configure(fg_color=color)

    def start_auto_play(self):
        if self.auto_play_task:
            self.after_cancel(self.auto_play_task)
        self.auto_play_task = self.after(4000, self.auto_next)

    def auto_next(self):
        if self.winfo_exists():
            next_idx = (self.carousel_index + 1) % len(self.carousel_images)
            self.animate_to(next_idx, direction=1)
            self.start_auto_play()

    def manual_slide(self, target_index):
        if self.is_animating or target_index == self.carousel_index:
            return
        
        direction = 1 if target_index > self.carousel_index else -1
        
        self.start_auto_play()
        self.animate_to(target_index, direction)

    def ease_in_out(self, t):
        return t * t * (3 - 2 * t)

    def animate_to(self, next_index, direction=1):
        if self.is_animating: return
        self.is_animating = True

        next_img = self.carousel_images[next_index]
        
        start_x_current = 0.5
        start_x_next = 0.5 + (1.0 * direction)
        
        self.next_label = ctk.CTkLabel(self.carousel_container, text="", image=next_img)
        self.next_label.place(relx=start_x_next, rely=0.45, anchor="center")
        
        self.next_label.lift()
        if self.dots_frame: self.dots_frame.lift()

        steps = 30
        delay = 15

        def step(i=0):
            if i > steps:
                self.carousel_current.destroy()
                self.carousel_current = self.next_label
                self.carousel_index = next_index
                self.update_dots()
                self.is_animating = False
                return

            p = i / steps
            
            eased_p = self.ease_in_out(p)

            current_target = 0.5 - (1.0 * direction * eased_p)
            
            next_target = start_x_next - (1.0 * direction * eased_p)

            self.carousel_current.place(relx=current_target, rely=0.45, anchor="center")
            self.next_label.place(relx=next_target, rely=0.45, anchor="center")

            self.after(delay, lambda: step(i + 1))

        step(0)

    def do_login(self):
        email = self.email_entry.get().strip()
        pw = self.password_entry.get().strip()

        if not email or not pw:
            messagebox.showwarning("Warning", "Mohon lengkapi data login.")
            return

        try:
            result = AkunController.prosesLogin(email, pw)
            if result["status"] == "SUCCESS":
                messagebox.showinfo("Success", "Login berhasil!")
                self.app.login_success(result["user"])
            else:
                messagebox.showerror("Error", result["message"])
        except NameError:
            messagebox.showinfo("Test Mode", f"Login UI Checked.\nEmail: {email}\nPass: {pw}")
