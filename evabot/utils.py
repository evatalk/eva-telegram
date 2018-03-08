class MessageInfoHandler(object):

    @classmethod
    def _get_user_id(cls, message):
        try:
            user_id = message['from']['id']
        except KeyError:
            # Adiconar um log com data e hora aonde o erro ocorreu.
            # lançar algum tipo de exceção.
            pass

        return user_id

    @classmethod
    def _get_user_first_name(cls, message):
        try:
            user_id = message['from']['first_name']
        except KeyError:
            # Adiconar um log com data e hora aonde o erro ocorreu.
            # lançar algum tipo de exceção.
            pass

        return user_id

    @classmethod
    def _get_sent_message_by_user(cls, message):
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
        body_data['message'] = cls._get_sent_message_by_user(message)
        body_data['user_first_name'] = cls._get_user_first_name(message)
        body_data['provider_user_id'] = cls._get_user_id(message)

        return body_data
        # return cls._get_sent_message_by_user(message)
