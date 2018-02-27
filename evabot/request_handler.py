import requests

class Requestor(object):

    @classmethod
    def post(cls, text_message):
        """Sends the user message to EVA's API"""

        request = requests.post(
            '0.0.0.0:8000', data = {'message': text_message})

        return request.text
        
