import os
import openai
from pathlib import Path
from learn_python.delphi.tutor import Tutor, ConfigurationError, TerminateSession
from learn_python.register import LLMBackends, Config
from learn_python.utils import lp_logger
from uuid import uuid1
import json
from pprint import pformat
from random import randint


class TestAITutor(Tutor):
    """
    This is a fake tutor implementation used to spoof tutoring for testing
    purposes.
    """

    api_key = None

    messages = []

    BACKEND = LLMBackends.TEST

    cycle = 0

    CYCLE_LIMIT = randint(2, 6)

    API_KEY_FILE = Path(__file__).parent / 'test_api.key'

    def __init__(self, api_key=api_key):
        super().__init__(api_key=api_key)
        if not self.api_key:
            lp_logger.info('No key available to launch TEST Tutor.')
            raise ConfigurationError(
                'The test tutor requires an api key to be installed. '
                'Please paste your TEST API key into the file: '
                f'{self.API_KEY_FILE.relative_to(os.getcwd())}.'
            )
        lp_logger.info('Initialized TEST Tutor.')

    def input(self, prompt):
        if self.cycle >= self.CYCLE_LIMIT:
            raise TerminateSession('Test Cycle limit reached')
        return f'cycle {self.cycle} input'

    async def send(self):
        self.logger.info('send()')
        resp = f'cycle {self.cycle} response'
        self.cycle += 1
        return resp

    def handle_response(self, response):
        # todo run any functions that were called out
        self.logger.info('handle_response(%s)', response)
        return response
