############################
# @author Elias De Hondt   #
# @since 01/01/2025        #
############################
# git clone https://github.com/EliasDeHondt/Internship.git
# cd Internship/scripts/aruba_monitor
# pip install -r requirements.txt
# pip install pyinstaller
# pyinstaller --onefile --icon=favicon.ico aruba_monitor.py
# dist/aruba_monitor.exe

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
    def __init__(self, api_version="v10.11"):
        self.api_version = api_version
        self.ip = None
        self.username = None
        self.password = None
        self.session_cookie = None
        self.cpu_data = []
        self.timestamps = []
        self.cpu_window = None

    def set_credentials(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password

    def get_session_cookie(self):
        if not all([self.ip, self.username, self.password]):
            return "Error: Missing credentials"
        
        login_url = f"https://{self.ip}/rest/{self.api_version}/login"
        try:
            response = requests.post(
                login_url, 
                data={"username": self.username, "password": self.password}, 
                verify=False, 
                timeout=10
            )
            response.raise_for_status()
            if response.cookies:
                self.session_cookie = dict(response.cookies)
                return self.session_cookie
            else:
                return "Failed"
        except requests.exceptions.RequestException as error:
            return f"Error: {error}"
    
    def Login(self, ip_entry, username_entry, password_entry):
        ip = ip_entry.get()
        username = username_entry.get()
        password = password_entry.get()

        if any(not value or value in ["|Enter Switch IP", "Enter Username", "Enter Password"] 
            for value in [ip, username, password]):
            messagebox.showerror("Input Error", "Please fill in all fields", parent=root)
            return

        self.set_credentials(ip, username, password)
        
        result = self.get_session_cookie()
        if isinstance(result, dict):
            messagebox.showinfo("Login Successful", "Login successful! Session cookie obtained.", parent=root)
        else:
            messagebox.showerror("Login Failed", f"{result}", parent=root)

    def get_interfaces(self):
        if not self.session_cookie:
            messagebox.showerror("Error", "Please log in first!", parent=root)
            return

        interfaces_url = f"https://{self.ip}/rest/{self.api_version}/system/interfaces"
        try:
            response = requests.get(interfaces_url, cookies=self.session_cookie, verify=False, timeout=10)
            response.raise_for_status()
            interfaces = response.json()

            self.show_interfaces(interfaces)
        except requests.exceptions.RequestException as error:
            messagebox.showerror("Error", f"Failed to retrieve interfaces: {error}", parent=root)

    def show_interfaces(self, interfaces):
        interface_window = tk.Toplevel(root)
        interface_window.title("The University of Buckingham - Interfaces")
        interface_window.geometry("400x500")
        interface_window.configure(bg=primary_color)

        icon_path = 'favicon.ico'
        if os.path.exists(icon_path):
            interface_window.wm_iconphoto(False, ImageTk.PhotoImage(Image.open(icon_path)))

        scrollbar = ttk.Scrollbar(interface_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(interface_window, bg=primary_color, fg=secondary_color, font=(font_name, 12), yscrollcommand=scrollbar.set)
        listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)

        for key in interfaces.keys():
            listbox.insert(tk.END, f"Interface name: {key}")

    def get_users(self):
        if not self.session_cookie:
            messagebox.showerror("Error", "Please log in first!", parent=root)
            return

        users_url = f"https://{self.ip}/rest/{self.api_version}/system/users"
        try:
            response = requests.get(users_url, cookies=self.session_cookie, verify=False, timeout=10)
            response.raise_for_status()
            users = response.json()

            self.show_users(users)
        except requests.exceptions.RequestException as error:
            messagebox.showerror("Error", f"Failed to retrieve users: {error}", parent=root)

    def show_users(self, users):
        user_window = tk.Toplevel(root)
        user_window.title("The University of Buckingham - Users")
        user_window.geometry("400x500")
        user_window.configure(bg=primary_color)

        icon_path = 'favicon.ico'
        if os.path.exists(icon_path):
            user_window.wm_iconphoto(False, ImageTk.PhotoImage(Image.open(icon_path)))

        scrollbar = ttk.Scrollbar(user_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(user_window, bg=primary_color, fg=secondary_color, font=(font_name, 12), yscrollcommand=scrollbar.set)
        listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)

        for user in users:
            listbox.insert(tk.END, f"User: {user.username}")

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
    root.geometry("500x350")
    root.resizable(False, False)
    root.configure(bg=primary_color)

    icon_path = 'favicon.ico'
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
    title_label = ttk.Label(main_frame, text="Aruba Monitor", font=(font_name, 20, "bold"), foreground=secondary_color)
    title_label.grid(row=0, column=1, pady=(0, 20))

    # Input IP
    ip_entry = ttk.Entry(main_frame, width=25, style="Rounded.TEntry")
    ip_entry.grid(row=1, column=1, pady=5)
    add_placeholder(ip_entry, "Enter Switch IP")

    # Input Username
    username_entry = ttk.Entry(main_frame, width=25, style="Rounded.TEntry")
    username_entry.grid(row=2, column=1, pady=5)
    add_placeholder(username_entry, "Enter Username")

    # Input Password
    password_entry = ttk.Entry(main_frame, width=25, show="*", style="Rounded.TEntry")
    password_entry.grid(row=3, column=1, pady=5)
    add_placeholder(password_entry, "Enter Password")

    # Button Login
    test_button = ttk.Button(main_frame, text="Login", command=lambda: monitor.Login(ip_entry, username_entry, password_entry))
    test_button.grid(row=4, column=0, pady=10)

    # Button Interface
    cpu_button = ttk.Button(main_frame, text="Get Interface", command=monitor.get_interfaces)
    cpu_button.grid(row=4, column=1, pady=5)

    # Button User
    cpu_button = ttk.Button(main_frame, text="Get User", command=monitor.get_users)
    cpu_button.grid(row=4, column=2, pady=5)

    # Footer
    footer = ttk.Label(root, text="Designed by The University of Buckingham", font=(font_name, 10), foreground=secondary_color, background=primary_color)
    footer.pack(side=tk.BOTTOM, pady=10)

    return root

monitor = ArubaMonitor(api_version="v10.11")
setup_ui(monitor).mainloop()