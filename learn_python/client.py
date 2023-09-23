from learn_python.register import Config
import requests
import time
import base64


class CourseClient:


    def signature(self):
        ts = str(int(time.time()))
        return {
            'X-Learn-Python-Repository': Config().origin,
            'X-Learn-Python-Timestamp': ts,
            'X-Learn-Python-Signature': base64.b64encode(Config().sign_message(ts)),
        }

    def register(self):
        resp = requests.get(f'{Config().server}/register/{Config().origin}', headers=self.signature())
        resp.raise_for_status()
        return Config().update({
            **resp.json(),
            'registered': True
        }).write()
    
    def get_tutor_auth(self):
        # todo signature scheme?
        resp = requests.get(
            f'{Config().server}/api/authorize_tutor',
            headers=self.signature()
        )
        resp.raise_for_status()
        return resp.json()

    def post_engagement(self, engagement):
        resp = requests.post(
            f'{Config().server}/api/engagement',
            json=engagement,
            headers=self.signature()
        )
        resp.raise_for_status()
        return resp.json()
