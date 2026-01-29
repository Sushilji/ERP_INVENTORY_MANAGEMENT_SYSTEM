from db.database import Database

class ReportRepository:
    def __init__(self, database: Database):
        self.database = database

    def stock_report(self):
        conn = self.database.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT i.ItemName, s.Quantity, u.UnitName
            FROM StockMaster s
            JOIN ItemMaster i ON s.ItemId = i.ItemId
            JOIN UnitMaster u ON i.UnitId = u.UnitId
        """)

        data = cursor.fetchall()
        conn.close()
        return data

    def sales_report(self):
        conn = self.database.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT so.SalesOrderNo,
                   c.DisplayName,
                   so.Amount,
                   so.Status,
                   so.CreatedOn
            FROM SalesOrder so
            JOIN CustomerMaster c
                 ON so.CustomerId = c.CustomerId
        """)

        data = cursor.fetchall()
        conn.close()
        return data

    def purchase_report(self):
        conn = self.database.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT p.PurchaseNo,
                   v.VendorName,
                   p.Amount,
                   p.CreatedOn
            FROM Purchase p
            JOIN VendorMaster v
                 ON p.VendorId = v.VendorId
        """)

        data = cursor.fetchall()
        conn.close()
        return data
