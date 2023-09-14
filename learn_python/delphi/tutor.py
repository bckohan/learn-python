import typer
import re
from pathlib import Path
import os
from contextlib import contextmanager
import subprocess
from functools import cached_property
from enum import Enum
from termcolor import colored
from typing import Optional, Union
from uuid import uuid1, UUID
from learn_python.tests.tasks import Task
from learn_python.tests.tests import tasks
from learn_python.doc import task_map, TaskMapper
import gzip
import json
from datetime import datetime
from dateutil.tz import tzlocal
from glob import glob


ROOT_DIR = Path(__file__).parent.parent.parent
LOG_DIR = ROOT_DIR / 'logs'


def now():
    return datetime.now(tz=tzlocal())


class TerminateSession(Exception):
    pass


class Tutor:
    """
    A base class for Tutor implementations. This class is responsible for the common tutoring tasks
    like defining the tutor's personality and fetching structured context regarding the gateway
    assignments and lessons. Implementations of tutors for specific LLMs or AI platforms should inherit 
    from this class.
    """

    # each session is given a unique identifier
    session_id: UUID = None
    session_history: list = None
    session_start: datetime = None
    session_end: datetime = None

    # if our session pertains to a particular task, they will be here
    task_test: Task = None
    task_docs: TaskMapper.AssignmentDocs = None

    LOG_RGX = re.compile('^delphi_(?P<id>[\w-]+)[.]json(?:[.](?P<ext>gz))?$')

    # accept tasks specified as their singular names, their pytest identifiers or the pytest function name
    TASK_NAME_RGX = re.compile('^((?:test_gateway[\d]*_)|(.*[:]{2}))?(?P<task_name>[\w]+)$')

    @property
    def me(self):
        return 'Delphi'
    
    @cached_property
    def origin(self):
        """The forked github repository - this will be used as the unique ID for the student"""
        try:
            return subprocess.run(['git', 'remote', 'get-url', 'origin'], capture_output=True, text=True).stdout
        except Exception:
            pass
        return None
    
    @cached_property
    def student(self):
        """The student's name is fetched from their git config install"""
        try:
            result = subprocess.run(['git', 'config', 'user.name'], capture_output=True, text=True)
            if result.stdout:
                name = result.stdout.split()[0]
                if len(name) > 1:
                    return name
            # if no name, use email instead
            if self.student_email:
                return self.student_email.split('@')[0]
        except Exception:
            pass
        return 'Student'
    
    @cached_property
    def student_email(self):
        """The student's email is fetched from their git config install"""
        try:
            result = subprocess.run(['git', 'config', 'user.email'], capture_output=True, text=True)
            return result.stdout
        except Exception:
            pass
        return None

    @property
    def directive(self):
        """Who is Delphi"""
        return (
            f'Your name is Delphi. My name is {self.student}. You are a friendly tutor who will '
            f'help me learn the Python programming language. You will not write the code for me even '
            f'if I ask, instead you will use natural language to explain any errors and suggest avenues '
            f'of approach. Please address me by my name.'
        )

    def send(self, message=None):
        """
        """
        raise NotImplementedError(f'Extending LLM backends must implement send according to its docstring.')

    def possible_tasks(self, task_name: str):
        mtch = self.TASK_NAME_RGX.match(task_name)
        if not mtch:
            raise RuntimeError(f'{task_name} is not a valid task name or identifier.')
        task_name = mtch.groupdict()['task_name']
        possibles = []
        for module, tasks in tasks.items():
            if task_name in tasks:
                possibles.append((module, tasks[task_name]))
        return possibles
            
    def start_session(self, task: Optional[Union[Task, str]] = None):
        self.session_id = uuid1()
        self.session_history = []
        self.session_start = now()
        self.session_end = None
        self.task_test = None
        self.task_docs = None
       
        print(colored(
            f'Waking {self.me} up, you may terminate the session by typing ctrl-D or kindly asking '
            f'{self.me} to go away.'
            , 'green'
        ))
        try:
            if isinstance(task, Task):
                self.task_test = task
            elif task and isinstance(task, str):
                possibles = self.possible_tasks(task)
                if not possibles:
                    raise RuntimeError(f'Unrecognized task: {task}')
                if len(possibles) == 1:
                    self.task_test = possibles[0][1]
                else:
                    while self.task_test is None:
                        input(f'Which task do you want help with?')

            if self.task_test:
                self.task_docs = task_map().get_task_doc(self.task_test.name)

            while True:
                self.get_response(self.init_agent())
                print(self.reply())

        except (TerminateSession, EOFError, KeyboardInterrupt):
            print(f'Goodbye!')
        
        self.session_end = now()
        self.log_session()
        self.submit_logs()

    def terminate(self):
        raise TerminateSession()
    
    def rerun(self):
        pass

    def log_session(self):
        try:
            with gzip.open(LOG_DIR / f'delphi_{self.session_id}.json.gz', 'wt', encoding='utf-8') as f:
                json.dump({
                    'id': self.session_id,
                    'origin': self.origin,
                    'student': self.student,
                    'email': self.email,
                    'start': self.session_start.isoformat(),
                    'end': self.session_end.isoformat(),
                    'tz_name': now().strftime('%Z'),
                    'tz_offset': now().utcoffset().total_seconds() // 3600,
                    'task': self.task_test.identifier if self.task_test else None,
                    'log': self.session_history
                }, f)
        except Exception:
            # this logging is not crucial - lets not confuse students if any errors pop up
            pass

    def submit_logs(self):
        logs = glob(LOG_DIR / 'delphi_*.json*')
        log_by_id = {}
        for log in logs:
            mtch = self.LOG_RGX.match(log)
            if mtch:
                log_by_id[mtch.groupdict()['id']] = {
                    'path': LOG_DIR / log,
                    'ext': mtch.groupdict().get('ext')
                }
        
        ids = list(log_by_id.keys())

        # get whichever sessions have not been recorded and submit them


@contextmanager
def delphi_context():
    assert ROOT_DIR.is_dir()
    start_dir = os.getcwd()
    os.chdir(ROOT_DIR)
    yield
    os.chdir(start_dir)


class LLMBackends(Enum):

    OPEN_AI = 'openai'

    def instantiate(self):
        if self is self.OPEN_AI:
            from learn_python.delphi.openai import OpenAITutor
            return OpenAITutor()
        else:
            raise NotImplementedError(f'{self} tutor backend is not implemented!')


_tutor = None
_explicitly_invoked = False
def tutor(llm = LLMBackends.OPEN_AI):
    """
    Get the active tutor, if this returns None then tutoring is not enabled.
    """
    global _tutor
    if _tutor and _tutor.backend is llm:
        return _tutor
    try:
        _tutor = llm.instantiate()
    except Exception as err:
        if _explicitly_invoked:
            raise err
    return _tutor


def delphi(
        task: Optional[str] = typer.Argument(None, help="The gateway task you need help with."),
        llm: LLMBackends = LLMBackends.OPEN_AI.value
):
    global _explicitly_invoked
    _explicitly_invoked = True
    """I need some help! Wake Delphi up!"""
    with delphi_context():
        try:
            tutor().start_session()
        except Exception as err:
            print(colored(str(err), 'red'))


def main():
    typer.run(delphi)
