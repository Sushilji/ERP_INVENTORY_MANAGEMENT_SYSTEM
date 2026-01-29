import pyodbc

class Database:
    def __init__(self):
        self.connection_string = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=DESKTOP-PNKV8PJ;"
            "DATABASE=INVENTORY_MANAGEMENT_SYSTEM;"
            "UID=sa;"
            "PWD=Admin@123;"
        )

    def get_connection(self):
        return pyodbc.connect(self.connection_string)