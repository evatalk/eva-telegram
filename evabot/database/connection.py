import records
from evabot.settings import DB

class Connection(object):
    def __init__(self):
        self.db = records.Database(DB)
    
    def get_token(self, telegram_id):
        pass

    def create_token(self, response, telegram_id):
        pass