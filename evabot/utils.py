class MessageInfoHandler(object):
    
    @classmethod
    def get_user_id(cls, response):
        try:
            user_id = response['from']['id']
        except KeyError:
            # Adiconar um log com data e hora aonde o erro ocorreu.
            # lançar algum tipo de exceção.
            pass

        return user_id

    @classmethod
    def get_sent_message_by_user(cls, response):
        try:
            message_sent = response['text']
        except KeyError:
            # Adiconar um log com data e hora aonde o erro ocorreu.
            # lançar algum tipo de exceção.
            pass
            
        return message_sent
