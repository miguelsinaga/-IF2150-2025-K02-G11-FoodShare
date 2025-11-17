# src/view/components/side_menu.py
import tkinter as tk

class SideMenu(tk.Frame):
    def __init__(self, parent, app, menu_items):
        """
        menu_items = [
            ("Dashboard", callback),
            ("Buat Donasi", callback),
            ("Daftar Request", callback),
            ...
        ]
        """
        super().__init__(parent, bg="#1F2937", width=220)
        self.app = app
        self.pack_propagate(False)

        tk.Label(self,
                 text="FoodDonate",
                 font=("Helvetica", 20, "bold"),
                 fg="white",
                 bg="#1F2937").pack(pady=25)

        for name, callback in menu_items:
            btn = tk.Button(
                self,
                text=name,
                font=("Helvetica", 12),
                bg="#1F2937",
                fg="white",
                activebackground="#374151",
                activeforeground="white",
                relief="flat",
                anchor="w",
                padx=20,
                command=callback
            )
            btn.pack(fill="x", pady=2)

        tk.Button(
            self,
            text="Logout",
            bg="#DC2626",
            fg="white",
            activebackground="#B91C1C",
            relief="flat",
            font=("Helvetica", 12, "bold"),
            command=self.logout
        ).pack(side="bottom", fill="x", pady=15)

    def logout(self):
        self.app.current_user = None
        self.app.show_frame("LoginPage")
