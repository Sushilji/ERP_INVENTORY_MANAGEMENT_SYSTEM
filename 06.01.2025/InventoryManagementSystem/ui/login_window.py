import tkinter as tk
from tkinter import messagebox
from db.database import Database
from repository.auth_repository import AuthRepository
from repository.permission_repository import PermissionRepository
from ui.main_window import MainWindow


class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("ERP Login")
        self.geometry("350x250")
        self.resizable(False, False)

        self.db = Database()
        self.auth_repo = AuthRepository(self.db)
        self.perm_repo = PermissionRepository(self.db)

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="ERP Login", font=("Arial", 16, "bold")).pack(pady=15)

        tk.Label(self, text="Email").pack()
        self.email_entry = tk.Entry(self, width=30)
        self.email_entry.pack()

        tk.Label(self, text="Password").pack(pady=(10, 0))
        self.password_entry = tk.Entry(self, width=30, show="*")
        self.password_entry.pack()

        tk.Button(
            self,
            text="Login",
            width=15,
            command=self.login
        ).pack(pady=20)

    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not email or not password:
            messagebox.showwarning("Validation", "Email and Password required")
            return

        user = self.auth_repo.authenticate(email, password)

        if not user:
            messagebox.showerror("Login Failed", "Invalid User Id Or Password")
            return

        permissions = self.perm_repo.get_permissions_by_role(user[2])

        self.destroy()
        app = MainWindow(user, permissions)
        app.mainloop()
