import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('weather_data.db')
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute('CREATE TABLE NOT');