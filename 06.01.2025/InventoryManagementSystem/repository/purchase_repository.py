from db.database import Database

class PurchaseRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_purchase(self, vendor_id, bill_no, amount):
        conn = self.database.get_connection()
        cursor = conn.cursor()

        # Get next Purchase No
        cursor.execute("EXEC dbo.GetNextPurchaseNo")
        purchase_no = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO Purchase
            (PurchaseNo, VendorId, BillNo, Amount)
            VALUES (?,?,?,?)
        """, (
            purchase_no,
            vendor_id,
            bill_no,
            amount
        ))

        conn.commit()
        conn.close()
        return purchase_no


    def get_all_purchases(self):
        conn = self.database.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT PurchaseId, PurchaseNo
            FROM Purchase
            ORDER BY PurchaseId
        """)

        rows = cursor.fetchall()
        conn.close()

        print("DEBUG: Purchases from DB =", rows)   # debug
        return rows

