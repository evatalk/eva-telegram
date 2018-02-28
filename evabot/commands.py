from request_handler import Requestor

class BotCommands(object):
    
    @classmethod
    def start(cls, bot, update):
        """Greetings message"""

        update.message.reply_text(
            'Bem-vindo, {}!!'.format(update.message.from_user.first_name))

        # bot.forward_message(update.message.chat_id, update.message.chat_id, update.message.message_id)


    @classmethod
    def ask_a_question(cls, bot, update):
        pass