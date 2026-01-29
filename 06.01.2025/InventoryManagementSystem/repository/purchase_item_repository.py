from db.database import Database

class PurchaseItemRepository:
    def __init__(self, database: Database):
        self.database = database

    def add_purchase_item(self, purchase_id, item_id, qty, rate):
        amount = qty * rate
        conn = self.database.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO PurchaseItem
            (PurchaseId, ItemId, Quantity, Rate, Amount)
            VALUES (?,?,?,?,?)
        """, (
            purchase_id,
            item_id,
            qty,
            rate,
            amount
        ))

        conn.commit()
        conn.close()
