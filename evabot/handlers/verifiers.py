from database.connection import Connection

class Verifier(object):
    @classmethod
    def is_registered(self, telegram_id):
        conn = Connection()
        user_data = conn.get_token(telegram_id)
        conn.close_connection()

        if user_data is None:
            return False

        return True
        
    @classmethod
    def is_in_the_first_step(self, telegram_id):
        conn = Connection()
        user_register_step = conn.get_step(telegram_id)
        conn.close_connection()

        return user_register_step is None