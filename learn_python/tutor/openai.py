import os
import openai
from pathlib import Path
from learn_python.tutor import Tutor

API_KEY_FILE = Path(__file__).parent / 'api.key'


response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a tutor who will help with my programming assignment. You will not write the code for me even if I ask."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"}
    ]
)


class OpenAITutor(Tutor):

    api_key = None
    model_priority = ['gpt-3.5-turbo', '']


    def __init__(self, api_key=api_key):

        if api_key is None and API_KEY_FILE.is_file():
            self.api_key = API_KEY_FILE.read_text().strip()
        
        if not self.api_key:
            raise RuntimeError(
                'The tutor requires an api key to be installed. '
                'Please create a file called api.key in the tutor '
                'directory and paste your openai API key into it.'
            )

    def start_session(self, gateway_assignment):
        use_tutor = input('Would you like assistance from the tutor? (y/n): ')
        if use_tutor.lower() in ['y', 'yes', 'true']:
            print('Starting tutor session...')
            self.tutor_session(gateway_assignment)
    
    def get_message(self, assignment):
        pass
