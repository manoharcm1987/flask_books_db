import sqlite3
import pathlib, os
from sqlite3 import Error


class DBHandler:

    DB_NAME = 'books.sqlite'

    def __init__(self):
        self.conn = None

    def create_connection(self):
        try:
            path = os.path.join(pathlib.Path(__file__).parent.absolute(), DBHandler.DB_NAME)
            self.conn = sqlite3.connect(path)
        except Error as e:
            print(e)
        return self.conn

    def create_table(self, table):
        cursor = self.conn.cursor()
        sql_query = " CREATE TABLE IF NOT EXISTS " + table + "(id integer PRIMARY KEY,author text NOT NULL," \
                    "language text NOT NULL,title text NOT NULL,price integer NOT NULL,published_year integer NOT NULL)"
        res = cursor.execute(sql_query)
        self.conn.commit()
        return f"Book with the id: {cursor.lastrowid} created successfully", 201

    def close_connection(self):
        if self.conn is not None:
            self.conn.close()


if __name__ == "__main__":
    db_conn = DBHandler()
    db_conn.create_connection()
    db_conn.create_table('books')
    db_conn.close_connection()
