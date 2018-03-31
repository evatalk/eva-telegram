from random import choice

from conversations.responses import RESPONSES
from database.connection import Connection
from database.map import USER_DATA
from handlers.reader import (CredentialsHandler, MessageInfoHandler,
                             ResponseHandlers)
from handlers.requestor import Requestor
from handlers.verifiers import Verifier
from handlers.writer import HistoryResponseWriter, Jsonifier
from settings import BOT


class EVAController(object):
    @classmethod
    def main(cls, msg):
        telegram_user_id = MessageInfoHandler.get_user_id(msg)

        if Verifier.is_registered(telegram_user_id):
            # Pesquisa o Token do usuário
            conn = Connection()
            query = conn.get_token(telegram_user_id)

            conn.close_connection()
            access_token = query[USER_DATA["ACCESS_TOKEN"]]
            return cls.request(access_token, msg)

        return cls.register_user(msg)

    @classmethod
    def register_user(self, msg):
        telegram_user_name = MessageInfoHandler.get_user_first_name(msg)
        telegram_user_id = MessageInfoHandler.get_user_id(msg)

        if Verifier.is_in_the_first_step(telegram_user_id):
            conn = Connection()
            conn.register_step(telegram_user_id)
            conn.update_step(telegram_user_id)
            # Registra número de tentativa de cadastro
            conn.register_trial(telegram_user_id)
            conn.close_connection()

            response = choice(RESPONSES["NOT_REGISTERED_MESSAGES"])
            return BOT.sendMessage(MessageInfoHandler.get_chat_id(msg), response)

        # Verificar qual o número de tentativa do usuário e atualizar
        # Se for igual a três, deverá bloquea-lo
        # Caso seja igual a três, comparar com o dia de hoje, caso seja menor
        # o trial deverá voltar para zero.
        # verificar dados e cadastrar usuário

        # Verifica se o usuário está bloqueado
        if Verifier.is_blocked(telegram_user_id):
            response = choice(RESPONSES["BLOCKED"])
            return BOT.sendMessage(MessageInfoHandler.get_chat_id(msg), response)

        # Verifica se o usuário já possui as três tentativas e está
        # apto a ser bloqueado
        if Verifier.is_blockeable(telegram_user_id):
            # bloquear o usuário e zerar o número de tentativas.
            conn = Connection()
            conn.update_blocked_date(telegram_user_id)
            conn.update_trial(telegram_user_id, 0)
            conn.close_connection()

            response = choice(RESPONSES["BLOCKED"])
            return BOT.sendMessage(MessageInfoHandler.get_chat_id(msg), response)

        # Recebe a mensagem enviada pelo usuário afim de retirar as credenciais
        user_credentials = MessageInfoHandler.get_sent_message_by_user(msg)

        try:
            email, cpf = CredentialsHandler.split(user_credentials)
        except ValueError:
            # Atualizar o trial
            conn = Connection()
            INDEX_NUMBER_OF_TRIALS = 0
            current_trial = conn.get_trial(telegram_user_id)
            trial = current_trial[INDEX_NUMBER_OF_TRIALS]
            conn.update_trial(telegram_user_id, int(trial) + 1)
            conn.close_connection()

            response = choice(RESPONSES["MALFORMED_MESSAGE_CREDENTIALS"])
            return BOT.sendMessage(MessageInfoHandler.get_chat_id(msg), response)

        if not Verifier.only_numbers(cpf):
            # Atualizar o trial
            conn = Connection()
            INDEX_NUMBER_OF_TRIALS = 0
            current_trial = conn.get_trial(telegram_user_id)
            trial = current_trial[INDEX_NUMBER_OF_TRIALS]
            conn.update_trial(telegram_user_id, int(trial) + 1)
            conn.close_connection()

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
            # Atualizar o trial
            conn = Connection()
            INDEX_NUMBER_OF_TRIALS = 0
            current_trial = conn.get_trial(telegram_user_id)
            trial = current_trial[INDEX_NUMBER_OF_TRIALS]
            conn.update_trial(telegram_user_id, int(trial) + 1)
            conn.close_connection()

            response = choice(RESPONSES["WRONG_CREDENTIALS"])
            return BOT.sendMessage(MessageInfoHandler.get_chat_id(msg), response)

        # Registra usuário no nosso banco de dados
        conn = Connection()
        conn.register_token(telegram_user_name, user_token, telegram_user_id)
        conn.close_connection()

        response = choice(RESPONSES["WELCOME"])
        BOT.sendMessage(MessageInfoHandler.get_chat_id(msg), response)

    @classmethod
    def request(cls, access_token, msg):
        request = Requestor()
        response = request.post(msg, access_token)

        intent = ResponseHandlers.get_intent(response)
        return cls.intent_map(msg, intent, response)

    @classmethod
    def intent_map(cls, msg, intent, response):
        if intent == "greetings":
            eva_message = ResponseHandlers.get_message(response)
            return BOT.sendMessage(MessageInfoHandler.get_chat_id(msg), eva_message)

        elif intent == "cursing":
            eva_message = ResponseHandlers.get_message(response)
            return BOT.sendMessage(MessageInfoHandler.get_chat_id(msg), eva_message)

        elif intent == "history":
            eva_response = ResponseHandlers.get_content(response)
            history = HistoryResponseWriter.concatenate_data(eva_response)
            for data in history:
                BOT.sendMessage(MessageInfoHandler.get_chat_id(msg), data)
            return

        elif intent == "certificate":
            eva_response = ResponseHandlers.get_content(response)
            try:
                BOT.sendMessage(MessageInfoHandler.get_chat_id(
                    msg), eva_response["after_2015"])
            except KeyError:
                pass
            try:
                BOT.sendMessage(MessageInfoHandler.get_chat_id(
                    msg), eva_response["between_2013_to_2014"])
            except KeyError:
                pass
            try:
                BOT.sendMessage(MessageInfoHandler.get_chat_id(
                    msg), eva_response["before_2013"])
            except KeyError:
                pass

            return

        elif intent == "open_to_subscription":
            return BOT.sendMessage(MessageInfoHandler.get_chat_id(msg), "Você não possui inscrições abertas no momento.")

        else:  # default
            eva_message = ResponseHandlers.get_message(response)
            return BOT.sendMessage(MessageInfoHandler.get_chat_id(msg), eva_message)
