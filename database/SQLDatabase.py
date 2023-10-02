import pyodbc
import pandas as pd

class SQLDatabase:

    def __init__(self, server, database, username, password):
        self.server = server
        self.database = database
        self.username = username
        self.password = password

    def connect(self):
        return pyodbc.connect(f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}")
    
    def get_data(self, query):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return data
    
    def get_data_frame(self, query):
        return pd.DataFrame(self.get_data(query))
    
    def insert_data(self, table_name, data):
        conn = self.connect()
        cursor = conn.cursor()
        columns = ", ".join(data.keys())
        values = ", ".join(["'" + str(value) + "'" for value in data.values()])
        sql_query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        cursor.execute(sql_query)
        conn.commit()
        conn.close()
