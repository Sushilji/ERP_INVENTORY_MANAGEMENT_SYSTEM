import tkinter as tk
from tkinter import messagebox

from db.database import Database
from repository.customer_repository import CustomerRepository


class CustomerWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Customer Master")
        self.geometry("1024x750")
        self.resizable(True, True)

        self.db = Database()
        self.customer_repo = CustomerRepository(self.db)

        self.create_widgets()
        self.load_customers()

    def create_widgets(self):
        tk.Label(self, text="Customer Master", font=("Arial", 14, "bold")).pack(pady=10)

        self.entries = {}

        # Customer Type
        tk.Label(self, text="Customer Type").pack(anchor="w", padx=20)
        self.customer_type = tk.StringVar(value="Individual")
        tk.OptionMenu(self, self.customer_type, "Individual", "Business").pack(padx=20, pady=5)

        fields = [
            ("Salutation (Mr/Ms/Mrs/Dr)", "salutation"),
            ("Name", "name"),
            ("Company Name", "company"),
            ("Display Name", "display_name"),
            ("Email", "email"),
            ("Phone", "phone"),
            ("Address", "address"),
            ("GST No (Business only)", "gst"),
            ("PAN No (Business only)", "pan"),
            ("Remark", "remark")
        ]

        for label, key in fields:
            tk.Label(self, text=label).pack(anchor="w", padx=20)
            entry = tk.Entry(self, width=55)
            entry.pack(padx=20, pady=3)
            self.entries[key] = entry

        tk.Button(
            self,
            text="Save Customer",
            width=22,
            command=self.save_customer
        ).pack(pady=15)

        self.customer_list = tk.Listbox(self, width=75, height=10)
        self.customer_list.pack(pady=10)

    def save_customer(self):
        try:
            self.customer_repo.add_customer(
                self.customer_type.get(),
                self.entries["salutation"].get(),
                self.entries["name"].get(),
                self.entries["company"].get(),
                self.entries["display_name"].get(),
                self.entries["email"].get(),
                self.entries["phone"].get(),
                self.entries["address"].get(),
                self.entries["gst"].get(),
                self.entries["pan"].get(),
                self.entries["remark"].get()
            )
            messagebox.showinfo("Success", "Customer saved successfully")
            self.clear_form()
            self.load_customers()
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def load_customers(self):
        self.customer_list.delete(0, tk.END)
        customers = self.customer_repo.get_all_customers()

        for c in customers:
            self.customer_list.insert(
                tk.END,
                f"{c[0]} | {c[1]} | {c[2]} | {c[3]} | {c[4]}"
            )

    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
