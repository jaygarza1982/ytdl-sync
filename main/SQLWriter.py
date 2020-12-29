import sqlite3
from sqlite3 import Error

class SQLWriter:
    def __init__(self, db_file):
        self.db_file = db_file
    
    def execute(self, sql, params=None):
        connection = None
        try:
            connection = sqlite3.connect(self.db_file)
            cursor = connection.cursor()
            if params == None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, params)
        except Error as e:
            print(e)
        finally:
            if connection:
                connection.commit()
                connection.close()

    def fetchall(self, sql, params=None):
        connection = None
        try:
            connection = sqlite3.connect(self.db_file)
            cursor = connection.cursor()
            if params == None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, params)
        except Error as e:
            print(e)
        finally:
            if connection:
                return cursor.fetchall()
                connection.close()
        return []

    def fetchone(self, sql, params=None):
        connection = None
        try:
            connection = sqlite3.connect(self.db_file)
            cursor = connection.cursor()
            if params == None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, params)
        except Error as e:
            print(e)
        finally:
            if connection:
                return cursor.fetchone()
                connection.close()
        return []