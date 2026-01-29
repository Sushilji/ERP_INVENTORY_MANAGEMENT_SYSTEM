import tkinter as tk
from tkinter import messagebox

from db.database import Database
from repository.unit_repository import UnitRepository


class UnitMasterWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Unit Master")
        self.geometry("400x350")
        self.resizable(False, False)

        self.db = Database()
        self.unit_repo = UnitRepository(self.db)

        self.create_widgets()
        self.load_units()

    def create_widgets(self):
        # Title
        tk.Label(
            self,
            text="Unit Master",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        # Unit Name
        tk.Label(self, text="Unit Name").pack(pady=(10, 0))
        self.unit_entry = tk.Entry(self, width=30)
        self.unit_entry.pack()

        # Save Button
        tk.Button(
            self,
            text="Save Unit",
            width=15,
            command=self.save_unit
        ).pack(pady=10)

        # Unit List
        self.unit_list = tk.Listbox(self, width=45, height=10)
        self.unit_list.pack(pady=10)

    def save_unit(self):
        unit_name = self.unit_entry.get().strip()

        if not unit_name:
            messagebox.showwarning("Validation", "Unit name is required")
            return

        try:
            self.unit_repo.add_unit(unit_name)
            messagebox.showinfo("Success", "Unit saved successfully")
            self.unit_entry.delete(0, tk.END)
            self.load_units()
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def load_units(self):
        self.unit_list.delete(0, tk.END)
        units = self.unit_repo.get_all_units()

        for unit in units:
            self.unit_list.insert(tk.END, f"{unit[0]} - {unit[1]}")
