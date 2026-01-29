import tkinter as tk
from tkinter import messagebox
from db.database import Database
from repository.user_repository import UserRepository
from utils.password_utils import PasswordUtils


class UserManagementWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("User Management")
        self.geometry("500x450")
        self.resizable(False, False)

        self.db = Database()
        self.user_repo = UserRepository(self.db)

        self.roles = {}
        self.create_widgets()
        self.load_roles()
        self.load_users()

    def create_widgets(self):
        tk.Label(self, text="User Name").pack(pady=(10, 0))
        self.name_entry = tk.Entry(self, width=40)
        self.name_entry.pack()

        tk.Label(self, text="Email").pack(pady=(10, 0))
        self.email_entry = tk.Entry(self, width=40)
        self.email_entry.pack()

        tk.Label(self, text="Password").pack(pady=(10, 0))
        self.password_entry = tk.Entry(self, width=40, show="*")
        self.password_entry.pack()

        tk.Label(self, text="Role").pack(pady=(10, 0))
        self.role_var = tk.StringVar()
        self.role_dropdown = tk.OptionMenu(self, self.role_var, "")
        self.role_dropdown.pack()

        tk.Button(
            self,
            text="Create User",
            width=20,
            command=self.create_user
        ).pack(pady=15)

        self.user_list = tk.Listbox(self, width=70, height=10)
        self.user_list.pack(pady=10)

    def load_roles(self):
        roles = self.user_repo.get_roles()
        menu = self.role_dropdown["menu"]
        menu.delete(0, "end")

        for role_id, role_name in roles:
            self.roles[role_name] = role_id
            menu.add_command(
                label=role_name,
                command=lambda r=role_name: self.role_var.set(r)
            )

        if roles:
            self.role_var.set(roles[0][1])

    def create_user(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        role_name = self.role_var.get()

        if not name or not email or not password:
            messagebox.showwarning("Validation", "All fields are required")
            return

        role_id = self.roles.get(role_name)
        password_hash = PasswordUtils.hash_password(password)

        try:
            self.user_repo.create_user(name, email, password_hash, role_id)
            messagebox.showinfo("Success", "User created successfully")
            self.clear_form()
            self.load_users()
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def load_users(self):
        self.user_list.delete(0, tk.END)
        users = self.user_repo.get_all_users()

        for u in users:
            self.user_list.insert(
                tk.END,
                f"{u[0]} | {u[1]} | {u[2]} | {u[3]}"
            )

    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
