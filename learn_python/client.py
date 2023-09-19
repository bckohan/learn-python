from learn_python.register import Config
import requests


class CourseClient:
    def register(self):
        return Config().update(
            {
                **requests.get(
                    f'{Config().server}/register/{Config().origin}',
                    raise_for_status=True
                ).json(),
                'registered': True
            }
        ).write()
    
    def get_tutor_auth(self):
        # todo signature scheme?
        return requests.get(
            f'{Config().server}/api/tutor/key',
            raise_for_status=True
        ).json()
