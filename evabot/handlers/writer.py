class Jsonifier(object):
    @classmethod
    def user_credentials(self, credentials):
        json_response = {
            "credentials": credentials,
        }

        return json_response


class HistoryResponseWriter(object):
    @classmethod
    def concatenate_data(cls, content):
        BASE = "Curso: {}\nSituação da matrícula: {}\nSituação da turma: {}"
        history = []
        for data in content:
            history.append(BASE.format(
                data["course_name"],
                data["enrollment_status"],
                data["class_status"],
            ))

        return history
