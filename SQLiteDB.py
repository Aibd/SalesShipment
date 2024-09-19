import sqlite3


class SqliteDBManager:
    def __init__(self, db_name):
        self.db_name = db_name

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.connection.close()
        if exc_val:
            raise

    def execute(self, query, params=None, fetch=False):
        if params:
            self.cursor.executemany(query, params)
        else:
            self.cursor.execute(query)
        if fetch:
            return self.cursor.fetchall()
        self.connection.commit()

    def insert(self, table, columns, values):
        columns_str = ', '.join(columns)
        placeholders = ', '.join('?' * len(columns))
        query = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})"
        self.execute(query, values)

    def update(self, table, set_columns, values):
        set_clause = ', '.join([f"{col} = ?" for col in set_columns])
        query = f"UPDATE {table} SET {set_clause} WHERE id = ?"
        self.execute(query, values)

    def delete(self, table, ids):
        query = f"DELETE FROM {table} WHERE id = ?"
        id_tuples = [(id_,) for id_ in ids]
        self.execute(query, id_tuples)


# if __name__ == "__main__":
#     # 初始化数据库并创建表结构
#     with SqliteDBManager('SalesShipment.db') as db:
#         # 创建表结构
#         with open('create_temp_table.sql', 'r') as f:
#             create_table_sql = f.read()
#         db.execute_query(create_table_sql)
