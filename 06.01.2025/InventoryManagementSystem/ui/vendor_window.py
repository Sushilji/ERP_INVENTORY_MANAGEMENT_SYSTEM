import tkinter as tk
from tkinter import messagebox

from db.database import Database
from repository.vendor_repository import VendorRepository


class VendorWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Vendor Master")
        self.geometry("500x500")
        self.resizable(False, False)

        self.db = Database()
        self.vendor_repo = VendorRepository(self.db)

        self.create_widgets()
        self.load_vendors()

    def create_widgets(self):
        tk.Label(self, text="Vendor Master", font=("Arial", 14, "bold")).pack(pady=10)

        self.entries = {}

        fields = [
            ("Vendor Name", "name"),
            ("Address", "address"),
            ("GST Type (SGST_CGST / IGST)", "gst_type"),
            ("GST No", "gst_no"),
            ("Contact No", "contact"),
            ("Mobile No", "mobile"),
            ("Email", "email")
        ]

        for label, key in fields:
            tk.Label(self, text=label).pack(anchor="w", padx=20)
            entry = tk.Entry(self, width=50)
            entry.pack(padx=20, pady=3)
            self.entries[key] = entry

        tk.Button(
            self,
            text="Save Vendor",
            width=20,
            command=self.save_vendor
        ).pack(pady=15)

        self.vendor_list = tk.Listbox(self, width=70, height=10)
        self.vendor_list.pack(pady=10)

    def save_vendor(self):
        try:
            self.vendor_repo.add_vendor(
                self.entries["name"].get(),
                self.entries["address"].get(),
                self.entries["gst_type"].get(),
                self.entries["gst_no"].get(),
                self.entries["contact"].get(),
                self.entries["mobile"].get(),
                self.entries["email"].get()
            )
            messagebox.showinfo("Success", "Vendor saved successfully")
            self.clear_form()
            self.load_vendors()
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def load_vendors(self):
        self.vendor_list.delete(0, tk.END)
        vendors = self.vendor_repo.get_all_vendors()

        for v in vendors:
            self.vendor_list.insert(
                tk.END,
                f"{v[0]} | {v[1]} | {v[2]} | {v[3]}"
            )

    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
