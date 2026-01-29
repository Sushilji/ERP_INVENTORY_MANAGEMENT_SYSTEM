from db.database import Database


class StockRepository:
    def __init__(self, database: Database):
        self.database = database

    def issue_stock(self, item_id, qty):
        conn = self.database.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            IF EXISTS (SELECT 1 FROM StockMaster WHERE ItemId = ?)
                UPDATE StockMaster
                SET Quantity = Quantity - ?, UpdatedOn = GETDATE()
                WHERE ItemId = ?
            ELSE
                INSERT INTO StockMaster (ItemId, Quantity)
                VALUES (?, -?)
            """,
            (item_id, qty, item_id, item_id, qty)
        )

        conn.commit()
        conn.close()

    def add_stock(self, item_id, qty):
        conn = self.database.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            IF EXISTS (SELECT 1 FROM StockMaster WHERE ItemId = ?)
                UPDATE StockMaster
                SET Quantity = Quantity + ?, UpdatedOn = GETDATE()
                WHERE ItemId = ?
            ELSE
                INSERT INTO StockMaster (ItemId, Quantity)
                VALUES (?, ?)
            """,
            (item_id, qty, item_id, item_id, qty)
        )

        conn.commit()
        conn.close()

