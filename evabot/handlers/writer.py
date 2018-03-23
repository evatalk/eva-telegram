class Jsonifier(object):
    @classmethod
    def user_credentials(self, email, cpf):
        json_response = {
            "email": email,
            "cpf": cpf,
        }

        return json_response