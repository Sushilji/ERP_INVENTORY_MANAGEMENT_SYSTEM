from db.database import Database

class SalesOrderRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_sales_order(self, customer_id, reference, amount):
        conn = self.database.get_connection()
        cursor = conn.cursor()

        # Step 1: Get next Sales Order No (pyodbc-safe)
        cursor.execute("EXEC GetNextSalesOrderNo")
        order_no = cursor.fetchone()[0]

        # Step 2: Insert Sales Order
        cursor.execute("""
            INSERT INTO SalesOrder
            (SalesOrderNo, CustomerId, Reference, Status, Amount, PaymentStatus)
            VALUES (?,?,?,?,?,?)
        """, (
            order_no,
            customer_id,
            reference,
            'OPEN',
            amount,
            'PENDING'
        ))

        conn.commit()
        conn.close()
        return order_no

    def get_all_sales_orders(self):
        conn = self.database.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT s.SalesOrderNo,
                   c.DisplayName,
                   s.Amount,
                   s.Status
            FROM SalesOrder s
            JOIN CustomerMaster c
                 ON s.CustomerId = c.CustomerId
            WHERE s.Is_Deleted = 0
        """)

        orders = cursor.fetchall()
        conn.close()
        return orders


