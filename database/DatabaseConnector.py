class DatabaseConnector:

    def connect(self):
        pass
    
    def disconnect(self):
        pass

    def execute_query(self, query):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        data = cursor.fetchall()
        self.disconnect(conn)
        return data

    def insert_data(self, table_name, schema_name, data):
        columns = ", ".join(data.keys())
        values = ", ".join(["'" + str(value) + "'" for value in data.values()])
        sql_query = f"INSERT INTO {schema_name}.{table_name} ({columns}) VALUES ({values})"
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(sql_query)
        conn.commit()
