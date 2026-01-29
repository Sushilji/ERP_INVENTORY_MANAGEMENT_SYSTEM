from db.database import Database
from repository.unit_repository import UnitRepository
from repository.item_group_repository import ItemGroupRepository
from repository.item_repository import ItemRepository
from repository.vendor_repository import VendorRepository
from repository.customer_repository import CustomerRepository


db = Database()
unit_repo = UnitRepository(db)
group_repo = ItemGroupRepository(db)
item_repo = ItemRepository(db)
vendor_repo = VendorRepository(db)
customer_repo = CustomerRepository(db)

print("1. Add Unit")
print("2. View Units")
print("3. Add Item Group")
print("4. View Item Groups")
print("5. Add Item")
print("6. View Items")
print("7. Add Vendor")
print("8. View Vendors")
print("9. Add Customer")
print("10. View Customers")

choice = input("Enter choice: ")

if choice == "1":
    name = input("Enter Unit Name: ")
    unit_repo.add_unit(name)
    print("Unit added successfully")

elif choice == "2":
    for u in unit_repo.get_all_units():
        print(u[0], "-", u[1])

elif choice == "3":
    name = input("Enter Item Group Name: ")
    group_repo.add_item_group(name)
    print("Item Group added successfully")

elif choice == "4":
    for g in group_repo.get_all_item_groups():
        print(g[0], "-", g[1])

elif choice == "5":
    item_name = input("Enter Item Name: ")
    group_id = int(input("Enter Item Group Id: "))
    unit_id = int(input("Enter Unit Id: "))
    item_repo.add_item(item_name, group_id, unit_id)
    print("Item added successfully")

elif choice == "6":
    for i in item_repo.get_all_items():
        print(i[0], "-", i[1], "|", i[2], "|", i[3])

if choice == "7":
    name = input("Vendor Name: ")
    address = input("Address: ")
    gst_type = input("GST Type (SGST_CGST / IGST): ")
    gst_no = input("GST No: ")
    contact = input("Contact No: ")
    mobile = input("Mobile No: ")
    email = input("Email: ")

    vendor_repo.add_vendor(name, address, gst_type, gst_no, contact, mobile, email)
    print("Vendor added successfully")

elif choice == "8":
    for v in vendor_repo.get_all_vendors():
        print(v[0], "-", v[1], "|", v[2], "|", v[3], "|", v[4])

elif choice == "9":
    ctype = input("Customer Type (Individual/Business): ")
    sal = input("Salutation (Mr/Ms/Mrs/Dr): ")
    cname = input("Contact Name: ")
    company = input("Company Name: ")
    dname = input("Display Name: ")
    email = input("Email: ")
    phone = input("Phone: ")
    address = input("Address: ")
    gst = input("GST No (optional): ")
    pan = input("PAN No (optional): ")
    remark = input("Remark: ")

    customer_repo.add_customer(
        ctype, sal, cname, company, dname,
        email, phone, address, gst, pan, remark
    )
    print("Customer added successfully")

elif choice == "10":
    for c in customer_repo.get_all_customers():
        print(c[0], "-", c[1], "|", c[2], "|", c[3], "|", c[4])
