import sqlite3

from evabot.settings import DB


class Connection(object):
    def __init__(self):
        self.conn = sqlite3.connect(DB)
        self.cursor = self.conn.cursor()

    def register_token(self, name, access_token, telegram_id):
        self.cursor.execute("""
            INSERT INTO users (nome, access_token, telegram_id)
            VALUES (?, ?, ?)
            """, (name, access_token, telegram_id))

        self.conn.commit()

    def get_token(self, telegram_id):
        self.cursor.execute(
            "SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))

        return self.cursor.fetchone()

    def register_step(self, telegram_id):
        self.cursor.execute("""
            INSERT INTO registerstep (step, telegram_id)
            VALUES (1, ?)
            """, (telegram_id))

        self.conn.commit()

    def update_step(self, telegram_id):
        self.cursor.execute("""
            UPDATE registerstep SET step = 2 WHERE telegram_id = ?    
            """, (telegram_id,))

    def get_step(self, telegram_id):
        self.cursor.execute(
            "SELECT step FROM registerstep WHERE telegram_id = ?", (telegram_id,))

        return self.cursor.fetchone()

    def close_connection(self):
        self.conn.close()
