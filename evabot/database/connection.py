import sqlite3

from evabot.settings import DB


class Connection(object):
    def __init__(self):
        self.conn = sqlite3.connect(DB)
        self.cursor = self.conn.cursor()

    def get_token(self, telegram_id):
        self.cursor.execute(
            "SELECT * FROM users where telegram_id = ?", (telegram_id,))
        return self.cursor.fetchone()

    def create_token(self, name, access_token, telegram_id):
        self.cursor.execute("""
            INSERT INTO users (nome, access_token, telegram_id)
            VALUES (?, ?, ?)
            """, (name, access_token, telegram_id))

        self.conn.commit()

    def close_connection(self):
        self.conn.close()
