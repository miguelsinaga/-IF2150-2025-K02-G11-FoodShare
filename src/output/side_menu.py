import customtkinter as ctk
from PIL import Image
import os

class SideMenu(ctk.CTkFrame):
    def __init__(self, parent, app, menu_items, active_item="Dashboard"):
        super().__init__(parent, fg_color="#132A13", width=250, corner_radius=0)
        self.app = app
        self.menu_items = menu_items
        self.active_item = active_item
        self.active_button = None

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
            if is_active:
                self.active_button = btn

        # --- LOGOUT BUTTON ---
        logout_frame = ctk.CTkFrame(self, fg_color="transparent")
        logout_frame.pack(side="bottom", fill="x", pady=30, padx=15)
        
        ctk.CTkButton(
            logout_frame,
            text="Logout",
            fg_color="transparent",
            text_color="#EF4444",
            font=("Arial", 14, "bold"),
            hover_color="#2D1F1F",  # Hover gelap kemerahan untuk logout
            anchor="w",
            cursor="hand2",  # Kursor tangan saat hover
            command=self.logout
        ).pack(fill="x")

        if self.active_button:
            self.animate_active_button(self.active_button, start_color="#BADA5F", end_color="#C5E064", steps=6, delay_ms=35)

    def create_menu_btn(self, text, command, is_active):
        # Logika warna hover dan aktif
        fg_color = "#C5E064" if is_active else "transparent"
        text_color = "#132A13" if is_active else "#A0B0A0"
        
        # Hover color: Jika aktif tetap sama, jika tidak aktif jadi hijau gelap sedikit terang
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
            cursor="hand2",  # Menambahkan kursor tangan
            command=command
        )
        return btn

    def animate_active_button(self, btn, start_color: str, end_color: str, steps: int = 6, delay_ms: int = 35):
        def hex_to_rgb(h: str):
            h = h.lstrip('#')
            return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

        def rgb_to_hex(rgb):
            return '#%02x%02x%02x' % rgb

        sr, sg, sb = hex_to_rgb(start_color)
        er, eg, eb = hex_to_rgb(end_color)

        def step(i=0):
            t = i / max(1, steps)
            cr = int(sr + (er - sr) * t)
            cg = int(sg + (eg - sg) * t)
            cb = int(sb + (eb - sb) * t)
            btn.configure(fg_color=rgb_to_hex((cr, cg, cb)))
            if i < steps:
                self.after(delay_ms, lambda: step(i + 1))

        step(0)

    def logout(self):
        self.app.current_user = None
        self.app.show_frame("LoginPage")
