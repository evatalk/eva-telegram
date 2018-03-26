import re


class MessageInfoHandler(object):

    @classmethod
    def get_user_id(cls, message):
        try:
            user_id = message['from']['id']
        except KeyError:
            # Adiconar um log com data e hora aonde o erro ocorreu.
            # lançar algum tipo de exceção.
            pass

        return user_id

    @classmethod
    def get_user_first_name(cls, message):
        try:
            user_id = message['from']['first_name']
        except KeyError:
            # Adiconar um log com data e hora aonde o erro ocorreu.
            # lançar algum tipo de exceção.
            pass

        return user_id

    @classmethod
    def get_sent_message_by_user(cls, message):
        try:
            message_sent = message['text']
        except KeyError:
            # Adiconar um log com data e hora aonde o erro ocorreu.
            # lançar algum tipo de exceção.
            pass

        return message_sent

    @classmethod
    def get_chat_id(cls, message):
        try:
            chat_id = message['chat']['id']
        except KeyError:
            # Adiconar um log com data e hora aonde o erro ocorreu.
            # lançar algum tipo de exceção.
            pass

        return chat_id

    @classmethod
    def serialized_data(cls, message):

        body_data = {}

        body_data['provider'] = "Telegram"
        body_data['message'] = cls.get_sent_message_by_user(message)
        body_data['user_first_name'] = cls.get_user_first_name(message)
        body_data['provider_user_id'] = cls.get_user_id(message)

        return body_data
        # return cls._get_sent_message_by_user(message)


class CredentialsHandler(object):
    @classmethod
    def split(cls, credentials):
        EMAIL_INDEX = 0
        CPF_INDEX = 1
        try:
            credentials_data = credentials.split(",")
            email = credentials_data[EMAIL_INDEX]
            cpf = credentials_data[CPF_INDEX]
        except (IndexError, ValueError):
            raise ValueError

        email = cls._format_email_to_request(email)
        cpf = cls._format_cpf_to_request(cpf)

        return email, cpf

    @classmethod
    def _format_cpf_to_request(cls, cpf):
        adjusted_cpf = "".join(
            re.split('[` \-=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>?]', cpf))
        return adjusted_cpf

    @classmethod
    def _format_email_to_request(cls, email):
        adjusted_email = "".join(re.split(" ", email))
        return adjusted_email


class ResponseHandlers(object):
    @classmethod
    def get_intent(cls, response):
        return response["intent"]

    @classmethod
    def get_content(cls, response):
        return response["content"]

    @classmethod
    def get_message(cls, response):
        return response["message"]
