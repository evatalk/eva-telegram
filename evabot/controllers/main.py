from random import choice

from conversations.responses import RESPONSES
from database.connection import Connection
from handlers.reader import CredentialsHandler, MessageInfoHandler
from handlers.requestor import Requestor
from handlers.verifiers import Verifier
from handlers.writer import Jsonifier
from settings import BOT


class EVAController(object):
    @classmethod
    def main(cls, msg):
        telegram_user_id = MessageInfoHandler.get_user_id(msg)

        if Verifier.is_registered(telegram_user_id):
            # TODO - Enviar msg para a API e criar map com as intenções
            return BOT.sendMessage(MessageInfoHandler.get_chat_id(msg), "Eae, men")

        return cls.register_user(msg)

    @classmethod
    def register_user(self, msg):
        # TODO - Conferir se o CPF é realmente válido, se consiste de números
        # Caso não seja, enviar msg pro usuário avisando da mal formatação.
        # - Criar mais mensagens de erro de formatação.
        telegram_user_name = MessageInfoHandler.get_user_first_name(msg)
        telegram_user_id = MessageInfoHandler.get_user_id(msg)

        if Verifier.is_in_the_first_step(telegram_user_id):
            conn = Connection()
            conn.register_step(telegram_user_id)
            conn.update_step(telegram_user_id)
            conn.close_connection()

            response = choice(RESPONSES["NOT_REGISTERED_MESSAGES"])
            return BOT.sendMessage(MessageInfoHandler.get_chat_id(msg), response)

        # verificar dados e cadastrar usuário
        user_credentials = MessageInfoHandler.get_sent_message_by_user(msg)

        try:
            email, cpf = CredentialsHandler.split(user_credentials)
        except ValueError:
            response = choice(RESPONSES["MALFORMED_MESSAGE_CREDENTIALS"])
            return BOT.sendMessage(MessageInfoHandler.get_chat_id(msg), response)

        # Confirma as credenciais - ALTERAR
        response = choice(RESPONSES["CONFIRM_CREDENTIALS"])
        BOT.sendMessage(MessageInfoHandler.get_chat_id(msg),
                        response.format(email, cpf))

        # Jsonifica as mensagens
        credentials = Jsonifier.user_credentials(email, cpf)

        # Enviar os dados Jsonificados para a API
        user_token = Requestor.register(credentials)

        # Verifica se a API retornou algum token
        if user_token is None:
            response = choice(RESPONSES["WRONG_CREDENTIALS"])
            return BOT.sendMessage(MessageInfoHandler.get_chat_id(msg), response)

        # Registra usuário no nosso banco de dados
        conn = Connection()
        conn.register_token(telegram_user_name, user_token, telegram_user_id)
        conn.close_connection()

        response = choice(RESPONSES["WELCOME"])
        BOT.sendMessage(MessageInfoHandler.get_chat_id(msg), response)

    def request(self, msg):
        # irá fazer a requisição para a API
        # e depois enviar a resposta para o response analisar
        pass
