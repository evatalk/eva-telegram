from random import choice

from conversations.responses import RESPONSES
from database.connection import Connection
from database.map import USER_DATA
from handlers.reader import (CredentialsHandler, MessageInfoHandler,
                             ResponseHandlers)
from handlers.requestor import Requestor
from handlers.verifiers import Verifier
from handlers.writer import (CertificateResponseWriter, HistoryResponseWriter,
                             Jsonifier)
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

            response = choice(RESPONSES["EVA_NOT_REGISTERED_MESSAGES"])
            return BOT.sendMessage(MessageInfoHandler.get_chat_id(msg), response)

        # Verificar qual o número de tentativa do usuário e atualizar
        # Se for igual a três, deverá bloquea-lo
        # Caso seja igual a três, comparar com o dia de hoje, caso seja menor
        # o trial deverá voltar para zero.
        # verificar dados e cadastrar usuário

        # Verifica se o usuário está bloqueado
        if Verifier.is_blocked(telegram_user_id):
            response = choice(RESPONSES["EVA_BLOCKED"])
            return BOT.sendMessage(MessageInfoHandler.get_chat_id(msg), response)

        # Verifica se o usuário já possui as três tentativas e está
        # apto a ser bloqueado
        if Verifier.is_blockeable(telegram_user_id):
            # bloquear o usuário e zerar o número de tentativas.
            conn = Connection()
            conn.update_blocked_date(telegram_user_id)
            conn.update_trial(telegram_user_id, 0)
            conn.close_connection()

            response = choice(RESPONSES["EVA_BLOCKED"])
            return BOT.sendMessage(MessageInfoHandler.get_chat_id(msg), response)

        # Recebe a mensagem enviada pelo usuário afim de retirar as credenciais
        received_message = MessageInfoHandler.get_sent_message_by_user(msg)

        extracted_cpf = CredentialsHandler.format_cpf_to_request(
            received_message)

        # Verifica se utilizando os manipuladores, conseguimos extrair o CPF
        # do usuário, caso seja, o received_message vira o número do CPF do usuário
        if Verifier.only_numbers(extracted_cpf):
            received_message = extracted_cpf

        # Caso não seja um CPF, verifica se é um e-mail
        # se não for, nós atualizaremos o número de tentativas
        # restantes do usuário.
        elif not Verifier.is_email(received_message):
            # Atualizar o trial
            conn = Connection()
            INDEX_NUMBER_OF_TRIALS = 0
            current_trial = conn.get_trial(telegram_user_id)
            trial = current_trial[INDEX_NUMBER_OF_TRIALS]
            conn.update_trial(telegram_user_id, int(trial) + 1)
            conn.close_connection()

            response = choice(RESPONSES["EVA_MALFORMED_MESSAGE_CREDENTIALS"])
            return BOT.sendMessage(MessageInfoHandler.get_chat_id(msg), response)

        # Jsonifica as mensagens
        credentials = Jsonifier.user_credentials(received_message)

        # Manda msg para usuário informando que a consulta está sendo feita.
        response = choice(RESPONSES["EVA_REGISTER_WAIT_MESSAGES"])
        BOT.sendMessage(MessageInfoHandler.get_chat_id(msg), response)

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

            response = choice(RESPONSES["EVA_WRONG_CREDENTIALS"])
            return BOT.sendMessage(MessageInfoHandler.get_chat_id(msg), response)

        # Registra usuário no nosso banco de dados
        conn = Connection()
        conn.register_token(telegram_user_name, user_token, telegram_user_id)
        conn.close_connection()

        response = choice(RESPONSES["EVA_WELCOME"])
        BOT.sendMessage(MessageInfoHandler.get_chat_id(msg), response)

    @classmethod
    def request(cls, access_token, msg):
        request = Requestor()

        # Envia uma mensagem para informar ao usuário que os dados
        # estão sendo processados
        wait_message = choice(RESPONSES["EVA_WAIT_MESSAGES"])
        BOT.sendMessage(MessageInfoHandler.get_chat_id(msg), wait_message)

        response = request.post(msg, access_token)

        intent = ResponseHandlers.get_intent(response)
        return cls.intent_map(msg, intent, response, access_token)

    @classmethod
    def intent_map(cls, msg, intent, response, access_token):
        if intent == "eva_greetings":
            response_message = choice(RESPONSES["EVA_GREETINGS"])
            return BOT.sendMessage(MessageInfoHandler.get_chat_id(msg), response_message)

        elif intent == "eva_how_are_you":
            response_message = choice(RESPONSES["EVA_HOW_ARE_YOU"])
            return BOT.sendMessage(MessageInfoHandler.get_chat_id(msg), response_message)

        elif intent == "eva_love":
            response_message = choice(RESPONSES["EVA_LOVE"])
            return BOT.sendMessage(MessageInfoHandler.get_chat_id(msg), response_message)

        elif intent == "eva_non_cursing":
            response_message = choice(RESPONSES["EVA_NON_CURSING"])
            return BOT.sendMessage(MessageInfoHandler.get_chat_id(msg), response_message)

        elif intent == "eva_hate":
            response_message = choice(RESPONSES["EVA_HATE"])
            return BOT.sendMessage(MessageInfoHandler.get_chat_id(msg), response_message)

        elif intent == "eva_description":
            response_message = choice(RESPONSES["EVA_DESCRIPTION"])
            return BOT.sendMessage(MessageInfoHandler.get_chat_id(msg), response_message)

        elif intent == "eva_thanks":
            response_message = choice(RESPONSES["EVA_THANKS"])
            return BOT.sendMessage(MessageInfoHandler.get_chat_id(msg), response_message)

        elif intent == "eva_user_history":
            eva_response = ResponseHandlers.get_content(response)

            history = HistoryResponseWriter.concatenate_data(eva_response)
            # Checa a fim de verificar se existem dados a serem exibidos.
            if not history:
                empty_message = choice(RESPONSES["EVA_EMPTY_RESPONSE"])
                return BOT.sendMessage(MessageInfoHandler.get_chat_id(msg), empty_message)

            # Envia uma mensagem pedindo desculpas pela demora
            apologize_message = choice(RESPONSES["EVA_APOLOGIZE"])
            BOT.sendMessage(MessageInfoHandler.get_chat_id(
                msg), apologize_message)

            # Itera sobre os dados do históricos informados pela API
            for data in history:
                BOT.sendMessage(MessageInfoHandler.get_chat_id(msg), data)

            return

        elif intent == "eva_user_certificate":
            eva_response = ResponseHandlers.get_content(response)

            # Envia uma mensagem pedindo desculpas pela demora
            apologize_message = choice(RESPONSES["EVA_APOLOGIZE"])

            BOT.sendMessage(MessageInfoHandler.get_chat_id(
                msg), apologize_message)

            # Informa ao usuário porque os certificados estão com instruções
            # de emissão diferentes
            information_about_certificates = choice(
                RESPONSES["EVA_INFORMATION_CERTIFICATE"])

            BOT.sendMessage(MessageInfoHandler.get_chat_id(
                msg), information_about_certificates)

            # Checa a fim de verificar se existem dados a serem exibidos.
            if (not eva_response["after_2015"]
                and not eva_response["between_2013_to_2014"]
                    and not eva_response["before_2013"]):

                empty_message = choice(RESPONSES["EVA_EMPTY_RESPONSE"])
                return BOT.sendMessage(MessageInfoHandler.get_chat_id(msg), empty_message)

            # Verifica se existe conteúdo na resposta da API
            # de acordo com a linha temporal
            if eva_response["after_2015"]:
                response_message = CertificateResponseWriter.after_2015_response(
                    eva_response["after_2015"])

                BOT.sendMessage(MessageInfoHandler.get_chat_id(
                    msg), response_message)

            if eva_response["between_2013_to_2014"]:
                response_message = CertificateResponseWriter.between_2013_to_2014_response(
                    eva_response["between_2013_to_2014"])

                BOT.sendMessage(MessageInfoHandler.get_chat_id(
                    msg), response_message)

            if eva_response["before_2013"]:
                response_message = CertificateResponseWriter.before_2013_response(
                    eva_response["before_2013"])

                BOT.sendMessage(MessageInfoHandler.get_chat_id(
                    msg), response_message)

            return

        elif intent == "eva_user_courses_open_to_subscription":
            # Envia uma mensagem pedindo desculpas pela demora
            apologize_message = choice(RESPONSES["EVA_APOLOGIZE"])
            BOT.sendMessage(MessageInfoHandler.get_chat_id(
                msg), apologize_message)
            # Está funcionalidade será desenvolvida futuramente
            return BOT.sendMessage(MessageInfoHandler.get_chat_id(msg), choice(RESPONSES["EVA_EMPTY_RESPONSE"]))

        elif intent == "eva_logout":
            telegram_user_id = MessageInfoHandler.get_user_id(msg)

            conn = Connection()
            # Desvincula o usuário do chatbot
            query = conn.delete_token(telegram_user_id)
            conn.close_connection()

            response_message = choice(RESPONSES["EVA_LOGOUT"])
            return BOT.sendMessage(MessageInfoHandler.get_chat_id(msg), response_message)

        else:  # default
            response_message = choice(RESPONSES["EVA_DEFAULT"])
            return BOT.sendMessage(MessageInfoHandler.get_chat_id(msg), response_message)
