from ui.login_window import LoginWindow

if __name__ == "__main__":
    LoginWindow().mainloop()





# from db.database import Database
# from repository.unit_repository import UnitRepository
# from repository.item_group_repository import ItemGroupRepository
# from repository.item_repository import ItemRepository
# from repository.vendor_repository import VendorRepository
# from repository.customer_repository import CustomerRepository
# from repository.sales_order_repository import SalesOrderRepository
# from repository.stock_repository import StockRepository
# from repository.sales_order_item_repository import SalesOrderItemRepository
# from repository.purchase_repository import PurchaseRepository
# from repository.purchase_item_repository import PurchaseItemRepository
# from repository.report_repository import ReportRepository


# db = Database()
# unit_repo = UnitRepository(db)
# group_repo = ItemGroupRepository(db)
# item_repo = ItemRepository(db)
# vendor_repo = VendorRepository(db)
# customer_repo = CustomerRepository(db)
# sales_repo = SalesOrderRepository(db)
# stock_repo = StockRepository(db)
# so_item_repo = SalesOrderItemRepository(db)
# purchase_repo = PurchaseRepository(db)
# purchase_item_repo = PurchaseItemRepository(db)
# report_repo = ReportRepository(db)



# print("1. Add Unit")
# print("2. View Units")
# print("3. Add Item Group")
# print("4. View Item Groups")
# print("5. Add Item")
# print("6. View Items")
# print("7. Add Vendor")
# print("8. View Vendors")
# print("9. Add Customer")
# print("10. View Customers")
# print("11. Create Sales Order")
# print("12. View Sales Orders")
# print("13. Add Item to Sales Order")
# print("14. View Stock")
# print("15. Create Purchase")
# print("16. Add Purchase Item")
# print("17. Stock Report")
# print("18. Sales Report")
# print("19. Purchase Report")

# choice = input("Enter choice: ")

# if choice == "1":
#     name = input("Enter Unit Name: ")
#     unit_repo.add_unit(name)
#     print("Unit added successfully")

# elif choice == "2":
#     for u in unit_repo.get_all_units():
#         print(u[0], "-", u[1])

# elif choice == "3":
#     name = input("Enter Item Group Name: ")
#     group_repo.add_item_group(name)
#     print("Item Group added successfully")

# elif choice == "4":
#     for g in group_repo.get_all_item_groups():
#         print(g[0], "-", g[1])

# elif choice == "5":
#     item_name = input("Enter Item Name: ")
#     group_id = int(input("Enter Item Group Id: "))
#     unit_id = int(input("Enter Unit Id: "))
#     item_repo.add_item(item_name, group_id, unit_id)
#     print("Item added successfully")

# elif choice == "6":
#     for i in item_repo.get_all_items():
#         print(i[0], "-", i[1], "|", i[2], "|", i[3])

# if choice == "7":
#     name = input("Vendor Name: ")
#     address = input("Address: ")
#     gst_type = input("GST Type (SGST_CGST / IGST): ")
#     gst_no = input("GST No: ")
#     contact = input("Contact No: ")
#     mobile = input("Mobile No: ")
#     email = input("Email: ")

#     vendor_repo.add_vendor(name, address, gst_type, gst_no, contact, mobile, email)
#     print("Vendor added successfully")

# elif choice == "8":
#     for v in vendor_repo.get_all_vendors():
#         print(v[0], "-", v[1], "|", v[2], "|", v[3], "|", v[4])

# elif choice == "9":
#     ctype = input("Customer Type (Individual/Business): ")
#     sal = input("Salutation (Mr/Ms/Mrs/Dr): ")
#     cname = input("Contact Name: ")
#     company = input("Company Name: ")
#     dname = input("Display Name: ")
#     email = input("Email: ")
#     phone = input("Phone: ")
#     address = input("Address: ")
#     gst = input("GST No (optional): ")
#     pan = input("PAN No (optional): ")
#     remark = input("Remark: ")

#     customer_repo.add_customer(
#         ctype, sal, cname, company, dname,
#         email, phone, address, gst, pan, remark
#     )
#     print("Customer added successfully")

# elif choice == "10":
#     for c in customer_repo.get_all_customers():
#         print(c[0], "-", c[1], "|", c[2], "|", c[3], "|", c[4])

# elif choice == "11":
#     cust_id = int(input("Customer Id: "))
#     ref = input("Reference: ")
#     amt = float(input("Amount: "))

#     so_no = sales_repo.create_sales_order(cust_id, ref, amt)
#     print("Sales Order Created:", so_no)

# elif choice == "12":
#     for s in sales_repo.get_all_sales_orders():
#         print(s[0], "|", s[1], "|", s[2], "|", s[3])

# elif choice == "13":
#     so_id = int(input("Sales Order Id: "))
#     item_id = int(input("Item Id: "))
#     qty = float(input("Quantity: "))
#     rate = float(input("Rate: "))

#     so_item_repo.add_item_to_order(so_id, item_id, qty, rate)
#     stock_repo.issue_stock(item_id, qty)

#     print("Item added to Sales Order and stock updated")

# elif choice == "14":
#     conn = db.get_connection()
#     cur = conn.cursor()
#     cur.execute("""
#         SELECT i.ItemName, s.Quantity
#         FROM StockMaster s
#         JOIN ItemMaster i ON s.ItemId = i.ItemId
#     """)
#     for r in cur.fetchall():
#         print(r[0], ":", r[1])
#     conn.close()

# elif choice == "15":
#     vendor_id = int(input("Vendor Id: "))
#     bill_no = input("Vendor Bill No: ")
#     amount = float(input("Total Amount: "))

#     p_no = purchase_repo.create_purchase(vendor_id, bill_no, amount)
#     print("Purchase Created:", p_no)

# elif choice == "16":
#     purchase_id = int(input("Purchase Id: "))
#     item_id = int(input("Item Id: "))
#     qty = float(input("Quantity: "))
#     rate = float(input("Rate: "))

#     purchase_item_repo.add_purchase_item(purchase_id, item_id, qty, rate)
#     stock_repo.add_stock(item_id, qty)

#     print("Purchase Item added and stock updated")

# elif choice == "17":
#     print("---- STOCK REPORT ----")
#     for r in report_repo.stock_report():
#         print(r[0], ":", r[1], r[2])

# elif choice == "18":
#     print("---- SALES REPORT ----")
#     for r in report_repo.sales_report():
#         print(r[0], "|", r[1], "|", r[2], "|", r[3], "|", r[4])

# elif choice == "19":
#     print("---- PURCHASE REPORT ----")
#     for r in report_repo.purchase_report():
#         print(r[0], "|", r[1], "|", r[2], "|", r[3])

# from ui.main_window import MainWindow

# if __name__ == "__main__":
#     app = MainWindow()
#     app.mainloop()


# # from ui.main_window import MainWindow

# # if __name__ == "__main__":
# #     app = MainWindow()
# #     app.mainloop()
