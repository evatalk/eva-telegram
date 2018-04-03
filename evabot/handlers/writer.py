from conversations.responses import RESPONSES


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


class CertificateResponseWriter(object):
    @classmethod
    def after_2015_response(cls, content):
        BASE_AFTER_2015 = RESPONSES["FINISHED_COURSES"]["after_2015"]
        finished_courses = cls._get_list_of_finished_courses(content)
        return cls._concatenate_information_to_text(BASE_AFTER_2015, finished_courses)

    @classmethod
    def between_2013_to_2014_response(cls, content):
        BASE_BETWEEN_2013_to_2014 = RESPONSES["FINISHED_COURSES"]["between_2013_to_2014"]
        finished_courses = cls._get_list_of_finished_courses(content)
        return cls._concatenate_information_to_text(BASE_BETWEEN_2013_to_2014, finished_courses)

    @classmethod
    def before_2013_response(cls, content):
        BASE_BEFORE_2013 = RESPONSES["FINISHED_COURSES"]["before_2013"]
        finished_courses = cls._get_list_of_finished_courses(content)
        return cls._concatenate_information_to_text(BASE_BEFORE_2013, finished_courses)

    @classmethod
    def _concatenate_information_to_text(cls, base_text, information_data):
        text_to_concatenate = ";\n- ".join(information_data)
        return base_text.format(text_to_concatenate)

    @classmethod
    def _get_list_of_finished_courses(self, dict_data):
        """
        From a list of dictionaries, returns a list
        containing the name of the courses.
        """
        course_names = []

        for data in dict_data:
            course_names.append(data["course_name"])

        return course_names
