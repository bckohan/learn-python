from learn_python.register import Config
from learn_python.utils import lp_logger, DateTimeEncoder
import requests
import time
import base64
import os
import json


class CourseClient:

    TIMEOUT_SECONDS = 20

    def signature(self):
        ts = str(int(time.time()))
        return {
            'X-Learn-Python-Repository': Config().origin,
            'X-Learn-Python-Timestamp': ts,
            'X-Learn-Python-Signature': base64.b64encode(Config().sign_message(ts)),
        }

    def register(self):
        resp = requests.get(
            f'{Config().server}/register/{Config().origin}',
            headers=self.signature(),
            timeout=self.TIMEOUT_SECONDS
        )
        resp.raise_for_status()
        return Config().update({
            **resp.json(),
            'registered': True
        }).write()
    
    def get_tutor_auth(self):
        resp = requests.get(
            f'{Config().server}/api/authorize_tutor',
            headers=self.signature(),
            timeout=self.TIMEOUT_SECONDS
        )
        resp.raise_for_status()
        return resp.json()

    def post_engagement(self, engagement):
        resp = requests.post(
            f'{Config().server}/api/engagements/',
            data=json.dumps(engagement, cls=DateTimeEncoder),
            headers={
                **self.signature(),
                'Content-Type': 'application/json'
            },
            timeout=self.TIMEOUT_SECONDS
        )
        resp.raise_for_status()
        lp_logger.info('Submitted engagement %s to server.', engagement.get('id', None))
        return resp.json()

    def post_log(self, log_path):
        log_path = str(log_path)
        assert log_path and os.path.exists(log_path)
        resp = requests.post(
            f'{Config().server}/api/logs/',
            files={'log': (os.path.basename(log_path), open(log_path, 'rb'))},
            headers=self.signature(),
            timeout=self.TIMEOUT_SECONDS
        )
        resp.raise_for_status()
        lp_logger.info('Submitted log %s to server.', os.path.basename(log_path))
        return resp.json()
