import os
import openai
from pathlib import Path
from learn_python.delphi.tutor import Tutor
from uuid import uuid1

API_KEY_FILE = Path(__file__).parent / 'openapi.key'


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
            raise RuntimeError(
                'The tutor requires an api key to be installed. '
                f'Please paste your OpenAI API key into the file: {API_KEY_FILE.relative_to(os.getcwd())}. '
                'See https://platform.openai.com/account/api-keys for details, or inquire with the instructor.'
            )
        
        openai.api_key = self.api_key

    @property
    def model(self):
        return self.model_priority[0]

    def prompt(self, task=None):
        use_tutor = input(f'Would you like assistance from {self.me}? (y/n): ')
        if use_tutor.lower() in ['y', 'yes', 'true']:
            print('Starting tutor session...')
            self.start_session(task=task)

    def start_session(self, task=None):

        import ipdb
        ipdb.set_trace()
    
    def init_agent(self, question):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.directive},
                {"role": "user", "content": question}
            ]
        )

    def format_message(self, question):
        pass
    
    def send(self, message):
        if message and isinstance(message, str):
            self.messages.append({'role': 'user', 'content': message})
        elif message and hasattr(message, '__iter__'):
            self.messages.extend(message)
        return openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages
        )

    def get_reply(self, response):
        return response['choices'][0]['message']['content']

    def process_response(self, response):
        pass

    @property
    def functions(self):
        funcs = [{
            'name': 'terminate',
            'description': 'Terminate the tutoring session.'
        }]
        if self.task_test:
            funcs.append({
                'name': 'rerun',
                'description': 'Re-execute the test for the task we are working on.'
            }
        )
        return funcs
