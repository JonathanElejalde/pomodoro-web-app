from typing import Union
import mysql.connector as connector
from mysql.connector import Error
import pandas as pd

from config import settings



class Database:

    def __init__(self) -> None:
        self.conn, self.cursor = self.create_connection()

    def create_connection(self):
        try:
            conn = connector.connect(
                host='localhost',
                database='pomodoros',
                user=settings.DATABASE_USER,
                password=settings.DATABASE_PASSWORD
            )
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
        
        cursor = conn.cursor()

        return conn, cursor

    def close_connection(self):
        if self.conn.is_connected():
            self.cursor.close()
            self.conn.close()

    def execute_query(self, query:str, values:Union[tuple, list[tuple]]):
        try:
            self.cursor.execute(query, values)
        except Exception as e:
            # This is a quick hack to solve the issue
            # Try to solve it in a cleaner way 

            # Add e to some log
            self.conn.reconnect()
            self.cursor.execute(query, values)

        self.conn.commit()

    def pandas_query(self, query:str, params:Union[tuple, list[tuple], dict] = ())-> pd.DataFrame:
        try:
            df = pd.read_sql(query, self.conn, params=params)
        except Exception as e:
            # Add e to some log
            self.conn.reconnect()
            df = pd.read_sql(query, self.conn, params=params)


        return df

DB = Database()

if __name__ == "__main__":
    pass