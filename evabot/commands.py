from request_handler import Requestor

class BotCommands(object):
    
    @classmethod
    def start(cls, bot, update):
        """Greetings message"""
    
        update.message.reply_text(
            'Bem-vindo, {}!!'.format(update.message.from_user.first_name))

    @classmethod
    def ask_a_question(cls, bot, update):
        pass