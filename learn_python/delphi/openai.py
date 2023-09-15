import os
import openai
from pathlib import Path
from learn_python.delphi.tutor import Tutor, ConfigurationError
from uuid import uuid1
import json

API_KEY_FILE = Path(__file__).parent / 'openai_api.key'


class OpenAITutor(Tutor):
    """
    https://platform.openai.com/docs/guides/gpt

    .. note::
    
        The OpenAI API is stateless, so each request needs to include the entire context
        the llm should respond to.
    """

    api_key = None
    model_priority = ['gpt-4', 'gpt-3.5-turbo']

    # this is a gpt parameter, None will use the default
    # Lower values for temperature result in more consistent
    # outputs, while higher values generate more diverse and 
    # creative results. Select a temperature value based on the 
    # desired trade-off between coherence and creativity for your 
    # specific application
    TEMPERATURE = None

    messages = []

    def __init__(self, api_key=api_key):

        if api_key is None and API_KEY_FILE.is_file():
            self.api_key = API_KEY_FILE.read_text().strip()
        
        if not self.api_key:
            with open(API_KEY_FILE, 'a'):
                os.utime(API_KEY_FILE, None)
            raise ConfigurationError(
                'The tutor requires an api key to be installed. '
                f'Please paste your OpenAI API key into the file: {API_KEY_FILE.relative_to(os.getcwd())}. '
                'See https://platform.openai.com/account/api-keys for details, or inquire with the instructor.'
            )
        
        openai.api_key = self.api_key

    def get_model(self, messages):
        # todo - return 32k model for large messages
        return self.model_priority[0]

    async def send(self):
        messages=[
            {'role': 'system', 'content': self.directive},
            *self.messages
        ]
        return await openai.ChatCompletion.acreate(
            model=self.get_model(messages),
            messages=messages,
            functions=self.functions
        )

    def handle_response(self, response):
        # todo run any functions that were called out
        resp = response['choices'][0]['message']
        to_call = {
            'terminate': self.terminate,
            'rerun': self.rerun
        }.get(resp.get('function_call', {}).get('name', None), None)
        if to_call:
            to_call(**json.loads(resp['function_call'].get('arguments', {})))
        return resp['content']

    @property
    def functions(self):
        funcs = [{
            'name': 'terminate',
            'description': 'Terminate the tutoring session.',
            'parameters': {
                'type': 'object',
                'properties': {},
                'required': []
            },
        }, {
            'name': 'set_task',
            'description': 'Determine which of the tasks .',
            'parameters': {
                'type': 'object',
                'properties': {},
                'required': []
            }
        }]
        if self.task_test:
            funcs.append({
                'name': 'rerun',
                'description': 'Re-execute the test for the task we are working on.',
                'parameters': {
                    'type': 'object',
                    'properties': {},
                    'required': []
                }
            }
        )
        return funcs
