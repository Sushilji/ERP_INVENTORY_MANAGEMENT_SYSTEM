from db.database import Database

class ItemRepository:
    def __init__(self, database: Database):
        self.database = database

    def add_item(self, item_name: str, group_id: int, unit_id: int):
        conn = self.database.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO ItemMaster (ItemName, ItemGroupId, UnitId)
            VALUES (?,?,?)
        """, (item_name, group_id, unit_id))

        conn.commit()
        conn.close()

    def get_all_items(self):
        conn = self.database.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT i.ItemId, i.ItemName, g.ItemGroupName, u.UnitName
            FROM ItemMaster i
            JOIN ItemGroupMaster g ON i.ItemGroupId = g.ItemGroupId
            JOIN UnitMaster u ON i.UnitId = u.UnitId
            WHERE i.Is_Deleted = 0
        """)

        items = cursor.fetchall()
        conn.close()
        return items
