#db connector file
import sqlite3

class FDatabase(object):
    def __init__(self, conn):
        self.conn = sqlite3.connect(conn + ".db")
    
    def migration(self):
        with open("schema.sql", "r") as f:
            lines = f.readlines()
            self.tables = "".join(lines)
            for item in self.tables.split(";"):
                 self.conn.cursor().execute(item + ";")
        return self.conn

class Repos(object):
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
        self.cursor = self.conn.cursor()
    
    def create_user(self, id, name, surname, code):
        query = f"INSERT INTO users (tg_id, name, surname, reffer_code) VALUES ({id},'{name}','{surname}','{code}')"
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            print(f"Вызвана ошибка {e}")
            raise e