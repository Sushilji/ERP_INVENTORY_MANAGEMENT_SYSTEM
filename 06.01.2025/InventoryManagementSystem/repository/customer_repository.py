from db.database import Database

class CustomerRepository:
    def __init__(self, database: Database):
        self.database = database

    def add_customer(
        self,
        customer_type,
        salutation,
        contact_name,
        company_name,
        display_name,
        email,
        phone,
        address,
        gst_no,
        pan_no,
        remark
    ):
        conn = self.database.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO CustomerMaster
            (CustomerType, Salutation, ContactName, CompanyName, DisplayName,
             Email, Phone, Address, GSTNo, PANNo, Remark)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """, (
            customer_type, salutation, contact_name, company_name,
            display_name, email, phone, address, gst_no, pan_no, remark
        ))

        conn.commit()
        conn.close()

    def get_all_customers(self):
        conn = self.database.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT CustomerId, DisplayName, CustomerType, Phone, GSTNo
            FROM CustomerMaster
            WHERE Is_Deleted = 0
        """)

        customers = cursor.fetchall()
        conn.close()
        return customers
