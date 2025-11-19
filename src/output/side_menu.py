import customtkinter as ctk
from PIL import Image
import os

class SideMenu(ctk.CTkFrame):
    def __init__(self, parent, app, menu_items, active_item="Dashboard"):
        super().__init__(parent, fg_color="#132A13", width=250, corner_radius=0)
        self.app = app
        self.menu_items = menu_items
        self.active_item = active_item

        # --- LOGO SECTION ---
        logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        logo_frame.pack(pady=(30, 30), padx=20, fill="x")

        # Load Logo
        image_path = "src/assets/logo2.png"
        # Fallback logo logic
        if not os.path.exists(image_path):
            # Try to find it in current dir just in case
            if os.path.exists("logo.png"): image_path = "logo.png"
            elif os.path.exists("Untitled design (2).png"): image_path = "Untitled design (2).png"

        if os.path.exists(image_path):
            try:
                pil_image = Image.open(image_path)
                self.logo_image = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(40, 40))
                ctk.CTkLabel(logo_frame, text="", image=self.logo_image).pack(side="left", padx=(0, 10))
            except:
                pass
        
        ctk.CTkLabel(logo_frame, text="FoodShare", font=("Arial", 24, "bold"), text_color="#E89D30").pack(side="left")

        # --- MENU ITEMS ---
        self.buttons = []
        for name, command in menu_items:
            is_active = (name == active_item)
            btn = self.create_menu_btn(name, command, is_active)
            btn.pack(fill="x", pady=5, padx=15)
            self.buttons.append(btn)

        # --- LOGOUT BUTTON ---
        logout_frame = ctk.CTkFrame(self, fg_color="transparent")
        logout_frame.pack(side="bottom", fill="x", pady=30, padx=15)
        
        ctk.CTkButton(
            logout_frame,
            text="Logout",
            fg_color="transparent",
            text_color="#EF4444",
            font=("Arial", 14, "bold"),
            hover_color="#2D1F1F",
            anchor="w",
            command=self.logout
        ).pack(fill="x")

    def create_menu_btn(self, text, command, is_active):
        fg_color = "#C5E064" if is_active else "transparent"
        text_color = "#132A13" if is_active else "#A0B0A0"
        hover_color = "#C5E064" if is_active else "#1F381F"
        
        btn = ctk.CTkButton(
            self,
            text=text,
            font=("Arial", 14, "bold"),
            fg_color=fg_color,
            text_color=text_color,
            hover_color=hover_color,
            anchor="w",
            height=45,
            corner_radius=10,
            command=command
        )
        return btn

    def logout(self):
        self.app.current_user = None
        self.app.show_frame("LoginPage")