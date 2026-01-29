from db.database import Database

class UnitRepository:
    def __init__(self, database: Database):
        self.database = database

    def add_unit(self, unit_name: str):
        conn = self.database.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO UnitMaster (UnitName)
            VALUES (?)
        """, unit_name)

        conn.commit()
        conn.close()

    def get_all_units(self):
        conn = self.database.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT UnitId, UnitName
            FROM UnitMaster
            WHERE Is_Deleted = 0
        """)

        units = cursor.fetchall()
        conn.close()
        return units
