import tkinter as tk
from tkinter import messagebox

from db.database import Database
from repository.item_group_repository import ItemGroupRepository


class ItemGroupWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Item Group Master")
        self.geometry("400x350")
        self.resizable(False, False)

        self.db = Database()
        self.group_repo = ItemGroupRepository(self.db)

        self.create_widgets()
        self.load_groups()

    def create_widgets(self):
        tk.Label(
            self,
            text="Item Group Master",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        tk.Label(self, text="Item Group Name").pack(pady=(10, 0))
        self.group_entry = tk.Entry(self, width=30)
        self.group_entry.pack()

        tk.Button(
            self,
            text="Save Item Group",
            width=18,
            command=self.save_group
        ).pack(pady=10)

        self.group_list = tk.Listbox(self, width=45, height=10)
        self.group_list.pack(pady=10)

    def save_group(self):
        group_name = self.group_entry.get().strip()

        if not group_name:
            messagebox.showwarning("Validation", "Item Group name is required")
            return

        try:
            self.group_repo.add_item_group(group_name)
            messagebox.showinfo("Success", "Item Group saved successfully")
            self.group_entry.delete(0, tk.END)
            self.load_groups()
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def load_groups(self):
        self.group_list.delete(0, tk.END)
        groups = self.group_repo.get_all_item_groups()

        for g in groups:
            self.group_list.insert(tk.END, f"{g[0]} - {g[1]}")
