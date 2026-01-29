from db.database import Database

class UserRepository:
    def __init__(self, database: Database):
        self.database = database

    def get_roles(self):
        conn = self.database.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT RoleId, RoleName
            FROM RoleMaster
            WHERE Is_Active = 1
        """)

        roles = cursor.fetchall()
        conn.close()
        return roles

    def create_user(self, name, email, password_hash, role_id):
        conn = self.database.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO UserMaster
            (UserName, Email, PasswordHash, RoleId)
            VALUES (?,?,?,?)
        """, (name, email, password_hash, role_id))

        conn.commit()
        conn.close()

    def get_all_users(self):
        conn = self.database.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT u.UserId, u.UserName, u.Email, r.RoleName
            FROM UserMaster u
            JOIN RoleMaster r ON u.RoleId = r.RoleId
        """)

        users = cursor.fetchall()
        conn.close()
        return users
