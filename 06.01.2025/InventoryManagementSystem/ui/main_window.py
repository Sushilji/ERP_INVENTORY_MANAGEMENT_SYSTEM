import tkinter as tk

from .unit_master_window import UnitMasterWindow
from .item_group_window import ItemGroupWindow
from .item_master_window import ItemMasterWindow
from .vendor_window import VendorWindow
from .user_management_window import UserManagementWindow
from .customer_window import CustomerWindow
from .sales_order_window import SalesOrderWindow
from .sales_order_item_window import SalesOrderItemWindow
from .purchase_window import PurchaseWindow
from .purchase_item_window import PurchaseItemWindow




class MainWindow(tk.Tk):
    def __init__(self, user, permissions):
        super().__init__()

        self.user = user
        self.permissions = permissions

        self.title("Inventory Management System")
        self.geometry("800x500")
        self.resizable(False, False)

        self.create_header()
        self.create_menu()

    def create_header(self):
        header = tk.Label(
            self,
            text=f"Inventory Management System | User: {self.user[1]} ({self.user[2]})",
            font=("Arial", 14, "bold"),
            bg="#2c3e50",
            fg="white",
            pady=15
        )
        header.pack(fill="x")

    def create_menu(self):
        frame = tk.Frame(self, pady=20)
        frame.pack()

        menu_items = [
            "Unit Master",
            "Item Group",
            "Item Master",
            "Vendor",
            "User Management",
            "Customer",
            "Sales",
            "Sales Items",
            "Purchase",
            "Purchase Items",
            "Exit"
        ]
        


        for i, name in enumerate(menu_items):
            btn = tk.Button(
                frame,
                text=name,
                width=22,
                height=2,
                command=lambda n=name: self.menu_action(n)
            )
            btn.grid(row=i // 3, column=i % 3, padx=15, pady=15)

    # INSIDE THE CLASS
    def menu_action(self, name):
        if name == "Unit Master":
            UnitMasterWindow(self)

        elif name == "Item Group":
            ItemGroupWindow(self)

        elif name == "Item Master":
            ItemMasterWindow(self)

        elif name == "User Management":
            UserManagementWindow(self)

        elif name == "Exit":
            self.destroy()
        
        elif name == "Vendor":
            VendorWindow(self)

        elif name == "Customer":
            CustomerWindow(self)
            
        elif name == "Sales":
            SalesOrderWindow(self)

        elif name == "Sales Items":
            SalesOrderItemWindow(self)

        elif name == "Purchase":
            PurchaseWindow(self)

        elif name == "Purchase Items":
            PurchaseItemWindow(self)



