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

class UserRepos(Repos):
    def create_user(self, id, name, surname, code):
        try:
            self.cursor.execute(f"INSERT INTO users (tg_id, name, surname, reffer_code) VALUES ({id},'{name}','{surname}','{code}')")
            self.conn.commit()
        except Exception as e:
            print(f"Вызвана ошибка {e}")
            raise e

class OrderRepos(Repos):
    def do_sub(self, date, id):
        if self.cursor.execute(f"SELECT busyby from orders WHERE date = {date}")[0] == 0:
            self.cursor.execute(f"UPDATE orders SET busyby = {id} WHERE date = {date}")
            self.conn.commit()
            return True

        return False
    
    def get_order_list(self):
        return self.cursor.execute(f"SELECT * FROM orders WHERE busyby = 0")

    def delete_sub(self, date, id):
        if self.cursor.execute(f"SELECT busyby from orders WHERE date = {date}")[0] == id:
            self.cursor.execute(f"UPDATE orders SET busyby = 0 WHERE date = {date}")
            self.conn.commit()
            return True
        return False
    
    def add_order(self, date):
        self.cursor.execute(f"INSERT INTO orders (timestamp, busyby) VALUES ({date}, {0})")
        self.conn.commit()
        return True