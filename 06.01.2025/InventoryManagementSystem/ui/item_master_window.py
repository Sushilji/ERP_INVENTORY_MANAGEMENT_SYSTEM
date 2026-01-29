import tkinter as tk
from tkinter import messagebox

from db.database import Database
from repository.item_repository import ItemRepository
from repository.item_group_repository import ItemGroupRepository
from repository.unit_repository import UnitRepository


class ItemMasterWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Item Master")
        self.geometry("450x450")
        self.resizable(False, False)

        self.db = Database()
        self.item_repo = ItemRepository(self.db)
        self.group_repo = ItemGroupRepository(self.db)
        self.unit_repo = UnitRepository(self.db)

        self.groups = {}
        self.units = {}

        self.create_widgets()
        self.load_groups()
        self.load_units()
        self.load_items()

    def create_widgets(self):
        tk.Label(self, text="Item Master", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(self, text="Item Name").pack()
        self.item_entry = tk.Entry(self, width=35)
        self.item_entry.pack()

        tk.Label(self, text="Item Group").pack(pady=(10, 0))
        self.group_var = tk.StringVar()
        self.group_menu = tk.OptionMenu(self, self.group_var, "")
        self.group_menu.pack()

        tk.Label(self, text="Unit").pack(pady=(10, 0))
        self.unit_var = tk.StringVar()
        self.unit_menu = tk.OptionMenu(self, self.unit_var, "")
        self.unit_menu.pack()

        tk.Button(
            self,
            text="Save Item",
            width=18,
            command=self.save_item
        ).pack(pady=15)

        self.item_list = tk.Listbox(self, width=60, height=10)
        self.item_list.pack(pady=10)

    def load_groups(self):
        groups = self.group_repo.get_all_item_groups()
        menu = self.group_menu["menu"]
        menu.delete(0, "end")

        for gid, gname in groups:
            self.groups[gname] = gid
            menu.add_command(
                label=gname,
                command=lambda g=gname: self.group_var.set(g)
            )

        if groups:
            self.group_var.set(groups[0][1])

    def load_units(self):
        units = self.unit_repo.get_all_units()
        menu = self.unit_menu["menu"]
        menu.delete(0, "end")

        for uid, uname in units:
            self.units[uname] = uid
            menu.add_command(
                label=uname,
                command=lambda u=uname: self.unit_var.set(u)
            )

        if units:
            self.unit_var.set(units[0][1])

    def save_item(self):
        name = self.item_entry.get().strip()
        group_name = self.group_var.get()
        unit_name = self.unit_var.get()

        if not name:
            messagebox.showwarning("Validation", "Item name is required")
            return

        group_id = self.groups.get(group_name)
        unit_id = self.units.get(unit_name)

        try:
            self.item_repo.add_item(name, group_id, unit_id)
            messagebox.showinfo("Success", "Item saved successfully")
            self.item_entry.delete(0, tk.END)
            self.load_items()
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def load_items(self):
        self.item_list.delete(0, tk.END)
        items = self.item_repo.get_all_items()

        for i in items:
            self.item_list.insert(
                tk.END,
                f"{i[0]} | {i[1]} | {i[2]} | {i[3]}"
            )
