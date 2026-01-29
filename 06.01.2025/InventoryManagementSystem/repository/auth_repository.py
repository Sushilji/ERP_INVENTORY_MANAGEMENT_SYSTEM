from db.database import Database
from utils.password_utils import PasswordUtils

class AuthRepository:
    def __init__(self, database: Database):
        self.database = database

    def authenticate(self, email, password):
        conn = self.database.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT u.UserId,
                   u.UserName,
                   u.PasswordHash,
                   r.RoleName
            FROM UserMaster u
            JOIN RoleMaster r
                 ON u.RoleId = r.RoleId
            WHERE u.Email = ?
              AND u.Is_Active = 1
              AND u.Is_Locked = 0
        """, (email,))

        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        if PasswordUtils.verify_password(password, row[2]):
            return (row[0], row[1], row[3])

        return None
