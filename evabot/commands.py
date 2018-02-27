
class BotCommands(object):
    
    @classmethod
    def start(cls, bot, update):
        """Greetings message"""
    
        update.message.reply_text(
            'Greetings, {}.'.format(update.message.from_user.first_name))
