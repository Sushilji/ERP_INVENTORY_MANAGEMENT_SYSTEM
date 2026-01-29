import tkinter as tk
from tkinter import messagebox

from db.database import Database
from repository.sales_order_repository import SalesOrderRepository
from repository.customer_repository import CustomerRepository


class SalesOrderWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Sales Order")
        self.geometry("1024x750")
        self.resizable(True, True)

        self.db = Database()
        self.sales_repo = SalesOrderRepository(self.db)
        self.customer_repo = CustomerRepository(self.db)

        self.customers = {}

        self.create_scrollable_frame()
        self.create_widgets()
        self.load_customers()

    # -------- Scrollable Base --------
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

        self.bind_all(
            "<MouseWheel>",
            lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        )

    # -------- UI --------
    def create_widgets(self):
        tk.Label(
            self.form,
            text="Sales Order",
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        # Customer
        tk.Label(self.form, text="Customer").pack(anchor="w", padx=20)
        self.customer_var = tk.StringVar()
        self.customer_menu = tk.OptionMenu(self.form, self.customer_var, "")
        self.customer_menu.pack(fill="x", padx=20, pady=5)

        # Reference
        tk.Label(self.form, text="Reference").pack(anchor="w", padx=20)
        self.ref_entry = tk.Entry(self.form)
        self.ref_entry.pack(fill="x", padx=20, pady=5)

        # Amount
        tk.Label(self.form, text="Total Amount").pack(anchor="w", padx=20)
        self.amount_entry = tk.Entry(self.form)
        self.amount_entry.pack(fill="x", padx=20, pady=5)

        tk.Button(
            self.form,
            text="Create Sales Order",
            width=25,
            command=self.create_sales_order
        ).pack(pady=20)

        self.result_lbl = tk.Label(self.form, text="", fg="green", font=("Arial", 11, "bold"))
        self.result_lbl.pack(pady=10)

    # -------- Data --------
    def load_customers(self):
        customers = self.customer_repo.get_all_customers()
        menu = self.customer_menu["menu"]
        menu.delete(0, "end")

        for cid, name, *_ in customers:
            self.customers[name] = cid
            menu.add_command(
                label=name,
                command=lambda n=name: self.customer_var.set(n)
            )

        if customers:
            self.customer_var.set(customers[0][1])

    def create_sales_order(self):
        try:
            cust_name = self.customer_var.get()
            customer_id = self.customers.get(cust_name)
            reference = self.ref_entry.get()
            amount = float(self.amount_entry.get())

            order_no = self.sales_repo.create_sales_order(
                customer_id, reference, amount
            )

            self.result_lbl.config(
                text=f"Sales Order Created Successfully : {order_no}"
            )
        except Exception as ex:
            messagebox.showerror("Error", str(ex))
