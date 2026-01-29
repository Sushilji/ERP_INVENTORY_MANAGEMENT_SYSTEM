import tkinter as tk
from tkinter import messagebox, ttk

from db.database import Database
from repository.purchase_repository import PurchaseRepository
from repository.purchase_item_repository import PurchaseItemRepository
from repository.item_repository import ItemRepository


class PurchaseItemWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Purchase Items")
        self.geometry("600x650")
        self.resizable(False, False)

        self.db = Database()
        self.purchase_repo = PurchaseRepository(self.db)
        self.purchase_item_repo = PurchaseItemRepository(self.db)
        self.item_repo = ItemRepository(self.db)

        self.purchases = {}   # {PurchaseNo: PurchaseId}
        self.items = {}       # {ItemName: ItemId}

        self.create_widgets()
        self.load_purchases()
        self.load_items()

        # Reload grid when purchase changes
        self.purchase_var.trace_add("write", self.on_purchase_change)

    # ---------------- UI ----------------
    def create_widgets(self):
        tk.Label(
            self,
            text="Purchase Items",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        # Purchase No
        tk.Label(self, text="Purchase No").pack(anchor="w", padx=20)
        self.purchase_var = tk.StringVar()
        self.purchase_menu = tk.OptionMenu(self, self.purchase_var, "")
        self.purchase_menu.config(width=25)
        self.purchase_menu.pack(padx=20, pady=5)

        # Item
        tk.Label(self, text="Item").pack(anchor="w", padx=20)
        self.item_var = tk.StringVar()
        self.item_menu = tk.OptionMenu(self, self.item_var, "")
        self.item_menu.config(width=25)
        self.item_menu.pack(padx=20, pady=5)

        # Quantity
        tk.Label(self, text="Quantity").pack(anchor="w", padx=20)
        self.qty_entry = tk.Entry(self, width=30)
        self.qty_entry.pack(padx=20, pady=5)

        # Rate
        tk.Label(self, text="Rate").pack(anchor="w", padx=20)
        self.rate_entry = tk.Entry(self, width=30)
        self.rate_entry.pack(padx=20, pady=5)

        tk.Button(
            self,
            text="Add Purchase Item",
            width=30,
            command=self.add_purchase_item
        ).pack(pady=15)

        # -------- Purchase Item Grid --------
        self.tree = ttk.Treeview(
            self,
            columns=("Item", "Quantity", "Rate", "Amount"),
            show="headings",
            height=10
        )

        self.tree.heading("Item", text="Item")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Rate", text="Rate")
        self.tree.heading("Amount", text="Amount")

        self.tree.column("Item", width=200)
        self.tree.column("Quantity", width=100)
        self.tree.column("Rate", width=100)
        self.tree.column("Amount", width=150)

        self.tree.pack(padx=20, pady=10, fill="x")

    # ---------------- LOAD DATA ----------------
    def load_purchases(self):
        purchases = self.purchase_repo.get_all_purchases()

        menu = self.purchase_menu["menu"]
        menu.delete(0, "end")
        self.purchases.clear()

        for p in purchases:
            purchase_id = p[0]     # INT
            purchase_no = p[1]     # PO-501

            self.purchases[purchase_no] = purchase_id

            menu.add_command(
                label=purchase_no,
                command=lambda n=purchase_no: self.purchase_var.set(n)
            )

        if purchases:
            self.purchase_var.set(purchases[0][1])
            self.load_purchase_items(purchases[0][0])

    def load_items(self):
        items = self.item_repo.get_all_items()

        menu = self.item_menu["menu"]
        menu.delete(0, "end")
        self.items.clear()

        for i in items:
            item_id = i[0]
            item_name = i[1]

            self.items[item_name] = item_id

            menu.add_command(
                label=item_name,
                command=lambda n=item_name: self.item_var.set(n)
            )

        if items:
            self.item_var.set(items[0][1])

    def load_purchase_items(self, purchase_id):
        self.tree.delete(*self.tree.get_children())

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT i.ItemName, pi.Quantity, pi.Rate, pi.Amount
            FROM PurchaseItem pi
            JOIN ItemMaster i ON pi.ItemId = i.ItemId
            WHERE pi.PurchaseId = ?
        """, (purchase_id,))

        rows = cursor.fetchall()
        conn.close()

        for r in rows:
            item_name = r[0]
            qty = float(r[1])
            rate = float(r[2])
            amount = float(r[3])

            self.tree.insert(
                "",
                tk.END,
                values=(
                    item_name,
                    f"{qty:.2f}",
                    f"{rate:.2f}",
                    f"{amount:.2f}"
                )
            )


    # ---------------- EVENTS ----------------
    def on_purchase_change(self, *args):
        purchase_no = self.purchase_var.get()
        purchase_id = self.purchases.get(purchase_no)

        if purchase_id:
            self.load_purchase_items(purchase_id)

    # ---------------- ACTION ----------------
    def add_purchase_item(self):
        purchase_no = self.purchase_var.get()
        item_name = self.item_var.get()

        purchase_id = self.purchases.get(purchase_no)
        item_id = self.items.get(item_name)

        if not purchase_id or not item_id:
            messagebox.showwarning(
                "Validation",
                "Please select Purchase and Item"
            )
            return

        try:
            qty = float(self.qty_entry.get())
            rate = float(self.rate_entry.get())
        except ValueError:
            messagebox.showerror(
                "Error",
                "Quantity and Rate must be numeric"
            )
            return

        try:
            self.purchase_item_repo.add_purchase_item(
                purchase_id,
                item_id,
                qty,
                rate
            )

            messagebox.showinfo(
                "Success",
                "Purchase item added and stock updated"
            )

            self.qty_entry.delete(0, tk.END)
            self.rate_entry.delete(0, tk.END)

            self.load_purchase_items(purchase_id)

        except Exception as ex:
            messagebox.showerror("Error", str(ex))
