import records
from evabot.settings import DB


class Connection(object):
    def __init__(self):
        self.db = records.Database(DB)

    def get_token(self, telegram_id):
        token_query = self.db.query(
            'select * from users where telegram_id = ' + telegram_id)
        
        if len(token_query) == 0:
            return None
        
        return token_query.first()

    def create_token(self, response, telegram_id):
        pass
