from random import choice

from conversations.responses import RESPONSES
from database.connection import Connection
from handlers.reader import MessageInfoHandler
from handlers.verifiers import Verifier
from settings import BOT


class EVAController(object):
    @classmethod
    def main(cls, msg):
        telegram_user_id = MessageInfoHandler.get_user_id(msg)

        if Verifier.is_registered(telegram_user_id):
            pass

        return cls.register_user(msg)

    @classmethod
    def register_user(self, msg):
        telegram_user_id = MessageInfoHandler.get_user_id(msg)
        if Verifier.is_in_the_first_step(telegram_user_id):
            conn = Connection()
            conn.register_step(telegram_user_id)
            conn.update_step(telegram_user_id)
            conn.close_connection()

            response = choice(RESPONSES["NOT_REGISTERED_MESSAGES"])
            return BOT.sendMessage(MessageInfoHandler.get_chat_id(msg), response)

        # verificar dados e cadastrar usuário
        # user_credentials = MessageInfoHandler.get_sent_message_by_user(msg)

    def request(self, msg):
        # irá fazer a requisição para a API
        # e depois enviar a resposta para o response analisar
        pass
