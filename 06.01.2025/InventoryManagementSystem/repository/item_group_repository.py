from db.database import Database

class ItemGroupRepository:
    def __init__(self, database: Database):
        self.database = database

    def add_item_group(self, group_name: str):
        conn = self.database.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO ItemGroupMaster (ItemGroupName)
            VALUES (?)
        """, group_name)

        conn.commit()
        conn.close()

    def get_all_item_groups(self):
        conn = self.database.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT ItemGroupId, ItemGroupName
            FROM ItemGroupMaster
            WHERE Is_Deleted = 0
        """)

        groups = cursor.fetchall()
        conn.close()
        return groups
