import psycopg2
from database.DatabaseConnector import DatabaseConnector

class PostgresSQLDatabaseConnector(DatabaseConnector):

    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password

    def connect(self):
        return psycopg2.connect(host=self.host, port=self.port, database=self.database, user=self.user, password=self.password)
    
    def disconnect(self, conn):
        conn.close()
    
    def execute_query(self, query):
        return super().execute_query(query)
    
    def insert_data(self, table_name, schema_name, data):
        return super().insert_data(table_name, schema_name, data)
    