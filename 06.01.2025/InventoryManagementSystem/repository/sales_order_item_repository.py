# from db.database import Database


# class SalesOrderItemRepository:
#     def __init__(self, database: Database):
#         self.database = database

#     def add_item_to_sales_order(self, sales_order_id, item_id, quantity, rate):
#         amount = quantity * rate

#         conn = self.database.get_connection()
#         cursor = conn.cursor()

#         # Insert item into sales order
#         cursor.execute(
#             """
#             INSERT INTO SalesOrderItem
#             (SalesOrderId, ItemId, Quantity, Rate, Amount)
#             VALUES (?,?,?,?,?)
#             """,
#             (sales_order_id, item_id, quantity, rate, amount)
#         )

#         # Update stock quantity
#         cursor.execute(
#             """
#             UPDATE Stock
#             SET Quantity = Quantity - ?, UpdatedOn = GETDATE()
#             WHERE ItemId = ?
#             """,
#             (quantity, item_id)
#         )

#         conn.commit()
#         conn.close()

from db.database import Database


class SalesOrderItemRepository:
    def __init__(self, database: Database):
        self.database = database

    def add_item_to_sales_order(self, sales_order_id, item_id, quantity, rate):
        conn = self.database.get_connection()
        cursor = conn.cursor()

        amount = quantity * rate

        # Insert sales order item (INT → INT mapping)
        cursor.execute("""
            INSERT INTO SalesOrderItem
            (SalesOrderId, ItemId, Quantity, Rate, Amount)
            VALUES (?,?,?,?,?)
        """, (
            sales_order_id,
            item_id,
            quantity,
            rate,
            amount
        ))

        # Deduct stock
        cursor.execute("""
            UPDATE Stock
            SET Quantity = Quantity - ?
            WHERE ItemId = ?
        """, (
            quantity,
            item_id
        ))

        conn.commit()
        conn.close()
