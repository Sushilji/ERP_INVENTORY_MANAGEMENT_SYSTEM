from db.database import Database

class VendorRepository:
    def __init__(self, database: Database):
        self.database = database

    def add_vendor(self, name, address, gst_type, gst_no, contact, mobile, email):
        conn = self.database.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO VendorMaster
            (VendorName, Address, GSTType, GSTNo, ContactNo, MobileNo, Email)
            VALUES (?,?,?,?,?,?,?)
        """, (name, address, gst_type, gst_no, contact, mobile, email))

        conn.commit()
        conn.close()

    def get_all_vendors(self):
        conn = self.database.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT VendorId, VendorName, GSTType, GSTNo, MobileNo
            FROM VendorMaster
            WHERE Is_Deleted = 0
        """)

        vendors = cursor.fetchall()
        conn.close()
        return vendors
