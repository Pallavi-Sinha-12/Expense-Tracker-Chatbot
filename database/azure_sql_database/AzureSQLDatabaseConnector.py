import pyodbc
from database.DatabaseConnector import DatabaseConnector

class AzureSQLDatabaseConnector(DatabaseConnector):

    def __init__(self, server, database, username, password):
        self.server = server
        self.database = database
        self.username = username
        self.password = password

    def connect(self):
        return pyodbc.connect(f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}")
    
    def disconnect(self, conn):
        conn.close()
        
    def execute_query(self, query):
        return super().execute_query(query)

    def insert_data(self, table_name, schema_name, data):
        return super().insert_data(table_name, schema_name, data)
        