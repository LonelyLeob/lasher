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
            self.cursor.execute(f"INSERT INTO users (tg_id, name, surname, reffer_code, reffer_quantity) VALUES ({id},'{name}','{surname}','{code}', 0)")
            self.conn.commit()
        except Exception as e:
            print(f"Вызвана ошибка {e}")
            raise e
    
    def get_all_users_id(self):
        try:
            return self.cursor.execute(f"SELECT tg_id FROM users").fetchall()
        except Exception as e:
            print(f"Вызвана ошибка {e}")
            raise e

    
    def profile(self, id:int):
        try:
            return self.cursor.execute(f"SELECT * FROM users WHERE tg_id = {id}").fetchone()
        except Exception as e:
            print(f"Вызвана ошибка {e}")
            raise e

class ScheduleRepos(Repos):
    def do_sub(self, date, ident):
        if self.cursor.execute(f"SELECT busyby from orders WHERE timestamp = {date}").fetchone()[0] == 0:
            self.cursor.execute(f"UPDATE orders SET busyby = {ident} WHERE timestamp = {date}")
            self.conn.commit()
    
    def get_free_order_list(self, now):
        return self.cursor.execute(f"SELECT timestamp FROM orders WHERE busyby = 0 AND timestamp >= {now}")

    def cancel_sub(self, date, id):
        if self.cursor.execute(f"SELECT busyby from orders WHERE timestamp = {date}")[0] == id:
            self.cursor.execute(f"UPDATE orders SET busyby = 0 WHERE timestamp = {date}")
            self.conn.commit()
    
    def add_order(self, date):
        try:
            self.cursor.execute(f"INSERT INTO orders (timestamp, busyby) VALUES ({date}, {0})")
            self.conn.commit()
        except Exception as e:
            print(f"Вызвана ошибка {e}")
            raise e

def user_exist(driver: sqlite3.Connection, id:int):
    return True if driver.cursor().execute(f"SELECT tg_id from users where tg_id = {id}").fetchone() != None else False
