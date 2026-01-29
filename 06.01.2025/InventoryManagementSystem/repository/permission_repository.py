from db.database import Database

class PermissionRepository:
    def __init__(self, database: Database):
        self.database = database

    def get_permissions_by_role(self, role_name):
        conn = self.database.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT rp.PermissionCode
            FROM RolePermission rp
            JOIN RoleMaster r
                 ON rp.RoleId = r.RoleId
            WHERE r.RoleName = ?
        """, (role_name,))

        permissions = [row[0] for row in cursor.fetchall()]
        conn.close()
        return permissions
