import re
from datetime import datetime

from database.connection import Connection


class Verifier(object):
    @classmethod
    def is_registered(cls, telegram_id):
        conn = Connection()
        user_data = conn.get_token(telegram_id)
        conn.close_connection()

        if user_data is None:
            return False

        return True

    @classmethod
    def is_in_the_first_step(cls, telegram_id):
        conn = Connection()
        user_register_step = conn.get_step(telegram_id)
        conn.close_connection()

        return user_register_step is None

    @classmethod
    def is_blocked(cls, telegram_id):
        conn = Connection()
        trials = conn.get_blocked_date(telegram_id)
        if trials:
            BLOCKED_DATE_INDEX = 0
            blocked_day = trials[BLOCKED_DATE_INDEX]
            if blocked_day == None:
                return False

            return blocked_day > datetime.now()

        return False

    @classmethod
    def is_blockeable(cls, telegram_id):
        conn = Connection()
        trials_tuple = conn.get_trial(telegram_id)
        if trials_tuple:
            INDEX_NUMBER_OF_TRIALS = 0
            trials = trials_tuple[INDEX_NUMBER_OF_TRIALS]
            return trials >= 3

        return False

    @classmethod
    def only_numbers(cls, entry):
        try:
            new_entry = int(entry)
        except ValueError:
            return False
        return True

    @classmethod
    def is_email(cls, entry):
        if re.match(r"[^@]+@[^@]+\.[^@]+", entry):
            return True
        return False
