############################
# @author Elias De Hondt   #
# @since 01/01/2025        #
############################

import requests
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import os

primary_color = "#1E1E1E"
secondary_color = "#FFFFFF"
accent_color = "#E9C43B"
hover_color = "#E9C05F"
font_name = "Helvetica"

class ArubaMonitor:
    def __init__(self, ip, username, password, api_version="v10.11"):
        self.ip = ip
        self.username = username
        self.password = password
        self.api_version = api_version

    def get_session_cookie(self):
        login_url = f"https://{self.ip}/rest/{self.api_version}/login"
        try:
            response = requests.post(login_url, data={"username": self.username, "password": self.password}, verify=False, timeout=10)
            response.raise_for_status()
            if response.cookies:
                return dict(response.cookies)
            else:
                return "Failed"
        except requests.exceptions.RequestException as error:
            return f"Error: {error}"
    
    def test_login(self):
        result = self.get_session_cookie()
        if isinstance(result, dict):
            messagebox.showinfo("Login Successful", f"{result}", parent=root)
        else:
            messagebox.showerror("Login Failed", f"{result}", parent=root)

def add_placeholder(entry, placeholder):
    entry.insert(0, placeholder)
    entry.config(foreground="grey")

    def on_focus_in(event):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(foreground=secondary_color)

    def on_focus_out(event):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(foreground="grey")

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

def setup_ui(monitor):
    global root
    root = tk.Tk()
    root.title("The University of Buckingham - Aruba Monitor")
    root.geometry("450x300")
    root.resizable(False, False)
    root.configure(bg=primary_color)

    icon_path = 'favicon.png'
    if os.path.exists(icon_path):
        root.wm_iconphoto(False, ImageTk.PhotoImage(Image.open(icon_path)))

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TLabel", background=primary_color, foreground=secondary_color, font=(font_name, 14))
    style.configure("TEntry", fieldbackground=primary_color, foreground=secondary_color, font=(font_name, 13), borderwidth=0, relief="flat", padding=5)
    style.configure("TButton", background=accent_color, foreground=secondary_color, font=(font_name, 14, "bold"), borderwidth=0, padding=5)
    style.map("TButton", background=[("active", hover_color)])

    style.element_create("Rounded.Entry", "from", "clam")
    style.configure("Rounded.TEntry", bordercolor=secondary_color, lightcolor=primary_color, darkcolor=primary_color, borderwidth=1)

    # Main frame
    main_frame = ttk.Frame(root, padding="20", style="Main.TFrame")
    main_frame.pack(expand=True)

    style.configure("Main.TFrame", background=primary_color)

    # Title label
    title_label = ttk.Label(main_frame, text="Aruba Monitor", font=(font_name, 18, "bold"), foreground=secondary_color)
    title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

    ip_entry = ttk.Entry(main_frame, width=25, style="Rounded.TEntry")
    ip_entry.grid(row=1, column=1, pady=5)
    add_placeholder(ip_entry, "Enter Switch IP")

    username_entry = ttk.Entry(main_frame, width=25, style="Rounded.TEntry")
    username_entry.grid(row=2, column=1, pady=5)
    add_placeholder(username_entry, "Enter Username")

    password_entry = ttk.Entry(main_frame, width=25, show="*", style="Rounded.TEntry")
    password_entry.grid(row=3, column=1, pady=5)
    add_placeholder(password_entry, "Enter Password")

    # Button
    test_button = ttk.Button(main_frame, text="Test Login", command=monitor.test_login)
    test_button.grid(row=4, column=0, columnspan=2, pady=20)

    # Footer
    footer = ttk.Label(root, text="Designed by The University of Buckingham", font=(font_name, 10), foreground=secondary_color, background=primary_color)  # Vergroot naar 10
    footer.pack(side=tk.BOTTOM, pady=10)

    return root


monitor = ArubaMonitor(ip="10.18.71.1", username="admin", password="GnR:sc0m", api_version="v10.11")
setup_ui(monitor).mainloop()