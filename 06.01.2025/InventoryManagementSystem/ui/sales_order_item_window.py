import tkinter as tk
from tkinter import messagebox

from db.database import Database
from repository.sales_order_item_repository import SalesOrderItemRepository
from repository.item_repository import ItemRepository
from repository.sales_order_repository import SalesOrderRepository


class SalesOrderItemWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Sales Order Items")
        self.geometry("1024x750")
        self.resizable(True, True)

        self.db = Database()
        self.item_repo = ItemRepository(self.db)
        self.so_repo = SalesOrderRepository(self.db)
        self.so_item_repo = SalesOrderItemRepository(self.db)

        self.items = {}    # {ItemName: ItemId}
        self.orders = {}   # {SalesOrderNo: SalesOrderId}

        self.create_scrollable_frame()
        self.create_widgets()
        self.load_items()
        self.load_orders()

    # ---------------- SCROLLABLE BASE ----------------
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

    # ---------------- UI ----------------
    def create_widgets(self):
        tk.Label(
            self.form,
            text="Sales Order Items",
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        # Sales Order
        tk.Label(self.form, text="Sales Order").pack(anchor="w", padx=20)
        self.order_var = tk.StringVar()
        self.order_menu = tk.OptionMenu(self.form, self.order_var, "")
        self.order_menu.pack(fill="x", padx=20, pady=5)

        # Item
        tk.Label(self.form, text="Item").pack(anchor="w", padx=20)
        self.item_var = tk.StringVar()
        self.item_menu = tk.OptionMenu(self.form, self.item_var, "")
        self.item_menu.pack(fill="x", padx=20, pady=5)

        # Quantity
        tk.Label(self.form, text="Quantity").pack(anchor="w", padx=20)
        self.qty_entry = tk.Entry(self.form)
        self.qty_entry.pack(fill="x", padx=20, pady=5)

        # Rate
        tk.Label(self.form, text="Rate").pack(anchor="w", padx=20)
        self.rate_entry = tk.Entry(self.form)
        self.rate_entry.pack(fill="x", padx=20, pady=5)

        tk.Button(
            self.form,
            text="Add Item to Sales Order",
            width=30,
            command=self.add_item
        ).pack(pady=20)

        self.msg_lbl = tk.Label(self.form, text="", fg="green", font=("Arial", 11, "bold"))
        self.msg_lbl.pack(pady=10)

    # ---------------- DATA LOAD ----------------
    def load_items(self):
        items = self.item_repo.get_all_items()

        menu = self.item_menu["menu"]
        menu.delete(0, "end")

        self.items.clear()

        for item in items:
            item_id = item[0]
            item_name = item[1]

            self.items[item_name] = item_id

            menu.add_command(
                label=item_name,
                command=lambda n=item_name: self.item_var.set(n)
            )

        if items:
            self.item_var.set(items[0][1])

    def load_orders(self):
        orders = self.so_repo.get_all_sales_orders()

        menu = self.order_menu["menu"]
        menu.delete(0, "end")

        self.orders.clear()

        for order in orders:
            order_id = order[0]     # INT
            order_no = order[1]     # SO-1002

            self.orders[order_no] = order_id

            menu.add_command(
                label=order_no,
                command=lambda o=order_no: self.order_var.set(o)
            )

        if orders:
            self.order_var.set(orders[0][1])

    # ---------------- ACTION ----------------
    def add_item(self):
        try:
            order_no = self.order_var.get()
            order_id = self.orders.get(order_no)

            item_name = self.item_var.get()
            item_id = self.items.get(item_name)

            qty = float(self.qty_entry.get())
            rate = float(self.rate_entry.get())

            if not order_id or not item_id:
                messagebox.showwarning("Validation", "Please select Sales Order and Item")
                return

            self.so_item_repo.add_item_to_sales_order(
                order_id, item_id, qty, rate
            )

            self.msg_lbl.config(text="Item added and stock updated successfully")

            self.qty_entry.delete(0, tk.END)
            self.rate_entry.delete(0, tk.END)

        except Exception as ex:
            messagebox.showerror("Error", str(ex))
