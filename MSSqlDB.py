import pyodbc
import configparser

class MSSqlDBManager:
    def __init__(self, AccountSet):
        self.config_file = 'config.ini'
        # AccountSet代表账套，上海账套使用"希肤上海"，广州账套使用"希肤广州"
        self.AccountSet = AccountSet
        self.config = self.load_config()
        self.connection = self._connect()

    def load_config(self):
        config = configparser.ConfigParser()
        config.read(self.config_file, encoding='utf-8')
        if self.AccountSet == '希肤广州':
            return config['DatabaseGZ']
        elif self.AccountSet == '希肤上海':
            return config['DatabaseSH']

    def __enter__(self):
        self.connection = self._connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()

    def _connect(self):
        connection_string = f"""
                    DRIVER={{SQL Server}};
                    SERVER={self.config['server']};
                    DATABASE={self.config['database']};
                    UID={self.config['username']};
                    PWD={self.config['password']};
                    Encrypt=no;
                """
        return pyodbc.connect(connection_string)

    def execute(self, command, params=None, fetch=False):
        with self.connection.cursor() as cursor:
            if params:
                cursor.executemany(command, params)
            else:
                cursor.execute(command)
            if fetch:
                return cursor.fetchall()
            self.connection.commit()

    def execute_delete(self,tablename, finterid, fentryid):
        sql = f"DELETE FROM {tablename} WHERE interid = ? AND entryid = ?"
        with self.connection.cursor() as cursor:
            cursor.execute(sql, (finterid, fentryid))
            self.connection.commit()
            return cursor.rowcount


    def close_connection(self):
        if self.connection:
            self.connection.close()

