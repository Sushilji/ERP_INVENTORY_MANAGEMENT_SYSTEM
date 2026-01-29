import tkinter as tk
from tkinter import messagebox

from db.database import Database
from repository.purchase_repository import PurchaseRepository
from repository.vendor_repository import VendorRepository


class PurchaseWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Purchase Entry")
        self.geometry("1024x750")
        self.resizable(True, True)

        self.db = Database()
        self.purchase_repo = PurchaseRepository(self.db)
        self.vendor_repo = VendorRepository(self.db)

        self.vendors = {}

        self.create_scrollable_frame()
        self.create_widgets()
        self.load_vendors()

    # ---------- Scroll ----------
    def create_scrollable_frame(self):
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)

        self.form = tk.Frame(canvas)

        self.form.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.form, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    # ---------- UI ----------
    def create_widgets(self):
        tk.Label(
            self.form,
            text="Purchase Entry",
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        # Vendor
        tk.Label(self.form, text="Vendor").pack(anchor="w", padx=20)
        self.vendor_var = tk.StringVar()
        self.vendor_menu = tk.OptionMenu(self.form, self.vendor_var, "")
        self.vendor_menu.pack(fill="x", padx=20, pady=5)

        # Vendor Bill No
        tk.Label(self.form, text="Vendor Bill No").pack(anchor="w", padx=20)
        self.bill_entry = tk.Entry(self.form)
        self.bill_entry.pack(fill="x", padx=20, pady=5)

        # Amount
        tk.Label(self.form, text="Total Amount").pack(anchor="w", padx=20)
        self.amount_entry = tk.Entry(self.form)
        self.amount_entry.pack(fill="x", padx=20, pady=5)

        tk.Button(
            self.form,
            text="Create Purchase",
            width=25,
            command=self.create_purchase
        ).pack(pady=20)

        self.msg_lbl = tk.Label(self.form, text="", fg="green", font=("Arial", 11, "bold"))
        self.msg_lbl.pack(pady=10)

    # ---------- Data ----------
    def load_vendors(self):
        vendors = self.vendor_repo.get_all_vendors()
        menu = self.vendor_menu["menu"]
        menu.delete(0, "end")

        self.vendors.clear()

        for v in vendors:
            vendor_id = v[0]
            vendor_name = v[1]

            self.vendors[vendor_name] = vendor_id

            menu.add_command(
                label=vendor_name,
                command=lambda n=vendor_name: self.vendor_var.set(n)
            )

        if vendors:
            self.vendor_var.set(vendors[0][1])

    def create_purchase(self):
        try:
            vendor_name = self.vendor_var.get()
            vendor_id = self.vendors.get(vendor_name)

            bill_no = self.bill_entry.get()
            amount = float(self.amount_entry.get())

            if not vendor_id or not bill_no:
                messagebox.showwarning("Validation", "Please enter all details")
                return

            purchase_no = self.purchase_repo.create_purchase(
                vendor_id, bill_no, amount
            )

            self.msg_lbl.config(
                text=f"Purchase Created Successfully : {purchase_no}"
            )

            self.bill_entry.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)

        except Exception as ex:
            messagebox.showerror("Error", str(ex))
