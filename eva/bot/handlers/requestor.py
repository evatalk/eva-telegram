import requests

from settings import EVA_HOST_URL

from .reader import MessageInfoHandler


class Requestor(object):

    @classmethod
    def post(cls, text_message, access_token):
        """Sends the user message to EVA's API"""

        # Caso você esteja rodando a API da EVA com o docker,
        # descubra qual o IP que a máquina docker está rodando e substitua
        # aqui embaixo. Caso contrário, não dará certo.

        # docker ps
        # docker inspect <hash_do_container>
        # procurar pelo campo "IPAddress"
        request = requests.post(f"http://{EVA_HOST_URL}/api/eva/request",
                                data=MessageInfoHandler.serialized_data(
                                    text_message),
                                headers={'Authorization': 'Token ' + access_token})

        return request.json()

    @classmethod
    def register(cls, credentials):
        request = requests.post(
            f"http://{EVA_HOST_URL}/api/eva/auth/register", data=credentials)

        if request.status_code == 201:
            return request.json()["token"]

        return None


class Response(object):

    @classmethod
    def request_to_response(cls, message, access_token):

        return Requestor.post(message, access_token)
