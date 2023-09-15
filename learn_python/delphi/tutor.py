import typer
import re
from pathlib import Path
import os
from contextlib import contextmanager, redirect_stdout, redirect_stderr
import subprocess
from functools import cached_property
from enum import Enum
from termcolor import colored
from typing import Optional, Union, List
from uuid import uuid1, UUID
from learn_python.tests.tasks import Task, TaskStatus
from learn_python.tests.tests import tasks
from learn_python.doc import task_map, TaskMapper
import gzip
import json
from datetime import datetime
from dateutil.tz import tzlocal
from glob import glob
from warnings import warn
import asyncio
import sys
from rich.console import Console
from rich.markdown import Markdown
from io import StringIO


ROOT_DIR = Path(__file__).parent.parent.parent
LOG_DIR = ROOT_DIR / 'logs'


def now():
    return datetime.now(tz=tzlocal())


class TerminateSession(Exception):
    pass


class RestartSession(Exception):
    pass


class ConfigurationError(Exception):
    pass
    

class Tutor:
    """
    A base class for Tutor implementations. This class is responsible for the common tutoring tasks
    like defining the tutor's personality and fetching structured context regarding the gateway
    assignments and lessons. Implementations of tutors for specific LLMs or AI platforms should inherit 
    from this class.

    todo:
        1) silence sphinx
        2) function for selecting task to get help with
        3) reload task when going from unimplemented to implemented
        4) log to web server
    """

    # each session is given a unique identifier
    engagement_id: UUID = None
    session_id: int = -1

    # the session message chain
    messages: List[str] = None
    session_start: datetime = None
    session_end: datetime = None

    # if our session pertains to a particular task, they will be here
    task_test: Task = None
    task_docs: TaskMapper.AssignmentDocs = None

    LOG_RGX = re.compile('^delphi_(?P<id>[\w-]+)_(?P<session>[\d]+)[.]json(?:[.](?P<ext>gz))?$')

    # accept tasks specified as their singular names, their pytest identifiers or the pytest function name
    TASK_NAME_RGX = re.compile('^((?:test_gateway[\d]*_)|(.*[:]{2}))?(?P<task_name>[\w]+)$')

    @property
    def me(self):
        return 'Delphi'
    
    @cached_property
    def origin(self):
        """The forked github repository - this will be used as the unique ID for the student"""
        try:
            return subprocess.run(
                ['git', 'remote', 'get-url', 'origin'],
                capture_output=True,
                text=True
            ).stdout
        except Exception:
            pass
        return None
    
    @cached_property
    def student(self):
        """The student's name is fetched from their git config install"""
        try:
            result = subprocess.run(
                ['git', 'config', 'user.name'],
                capture_output=True,
                text=True
            )
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
        """Who is the tutor?"""
        return (
            f'Your name is {self.me}. My name is {self.student}. You are a friendly and encouraging tutor who '
            f'will help me learn the Python programming language. You will not write any code for me even '
            f'if I ask, instead you will use natural language to explain any errors and suggest avenues '
            f'of approach. Please address me by my name.'
        )

    def prompt(self, task=None):
        use_tutor = input(f'Would you like assistance from {self.me}? (y/n): ')
        if use_tutor.lower() in ['y', 'yes', 'true']:
            print('Starting tutor session...')
            self.start_session(task=task)
    
    async def spinner(self):
        symbols = ['|', '/', '-', '\\']
        while True:
            for symbol in symbols:
                sys.stdout.write(f'\r{symbol}')
                sys.stdout.flush()
                await asyncio.sleep(0.1)

    async def get_response(self, message=''):
        """
        Get the response to the message from the user. If no message, rely on whats
        on the messages stack. This will display a progress spinner on the terminal
        until send completes and a response is available.
        """
        if message:
            self.push('user', message)
        spinner_task = asyncio.create_task(self.spinner())
        response = await self.send()
        spinner_task.cancel()
        sys.stdout.write('\r')
        sys.stdout.flush()
        return response
    
    async def send(self):
        """
        Send the message chain and return a response.
        """
        raise NotImplementedError(
            f'Extending LLM backends must implement send according to its docstring.'
        )
    
    def handle_response(self, response):
        """
        Process the response object and return the message from it. If the response asks for any functions
        to be called, they should be executed here.
        """
        raise NotImplementedError(
            f'Extending LLM backends must implement handle_response according to its docstring.'
        )
    
    def possible_tasks(self, task_name: str):
        mtch = self.TASK_NAME_RGX.match(task_name)
        if not mtch:
            raise RuntimeError(f'{task_name} is not a valid task name or identifier.')
        task_name = mtch.groupdict()['task_name']
        possibles = []
        for module, mod_tasks in tasks.items():
            if task_name in mod_tasks:
                possibles.append((module, mod_tasks[task_name]))
        return possibles
    
    def init_for_task(self):
        """Reinitialize AI tutor context for help with the set tasks"""
        # sanity check
        assert self.task_test and self.task_docs, f'Cannot initialize {self.me} for a task without a test and documentation to rely on.'
        self.task_test.run()
        message = f'I have been assigned the following task:\n{self.task_docs.todo}\n'
        if self.task_docs.requirements:
            reqs = "\n".join(self.task_docs.requirements)
            message += f'It has the following requirements:\n{reqs}\n'
        if self.task_docs.hints:
            hints = "\n".join(self.task_docs.hints)
            message += f'I have been given the following hints: \n{hints}\n'
        message += f'My current implementation looks like:\n{self.task_test.implementation}'
        self.push('user', message.strip())
        

    def push(self, role, message=''):
        """Add message to history"""
        if message:
            self.messages.append({'role': role, 'content': message})
        return message

    def init(
            self,
            task: Optional[Union[Task, str]] = None,
            notice: Optional[str] =  colored(
                f'Waking up, you may terminate the session by typing ctrl-D or kindly asking '
                f'me to go away.',
                'green'
        )
    ):
        try:
            self.start_session(task=task, notice=notice)
        except RestartSession as err:
            # a little tail recursion never hurt anybody
            self.init(task=self.task_test, notice=str(err))

    def start_session(
        self,
        task: Optional[Union[Task, str]] = None,
        notice: str = ''
    ):
        self.engagement_id = self.engagement_id or uuid1()
        self.session_id += 1
        self.messages = []
        self.session_start = now()
        self.session_end = None
        self.task_test = None
        self.task_docs = None
        
        if notice:
            print(notice)
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
                        prompt = f'Which task do you want help with?:\n'
                        for idx, candidate in enumerate(possibles):
                            prompt += f'[{idx}] {candidate[0]}: {candidate[1].name}'
                        try:
                            self.task_test = possibles[int(input(prompt))][1]
                        except (TypeError, ValueError, IndexError):
                            print(f'unrecognized.')
                            continue

            if self.task_test:
                out = StringIO()

                print(f'%%%%%%%%%%%%%')
                with redirect_stdout(out):
                    with redirect_stderr(out):
                        self.task_docs = task_map().get_task_doc(self.task_test.module, self.task_test.name)
                print(f'%%%%%%%%%%%%%')
                if self.task_docs:
                    self.init_for_task()
                else:
                    # this shouldn't be possible if doc check is passing,
                    # unless students delete docs
                    warn(
                        f'Unable to resolve instructions for task: '
                        f'[{self.task_test.module}] {self.task_test.name}, {self.me} '
                        f'will not have the needed context.'
                    )

            first = True
            console = Console()
            while True:
                console.print(
                    Markdown(
                        self.push(
                            'assistant',
                            self.handle_response(
                                asyncio.run(
                                    self.get_response('' if first and self.messages else input())
                                )
                            )
                        )
                    )
                )
                first = False

        except (TerminateSession, EOFError, KeyboardInterrupt):
            print(f'Goodbye.')
        finally:
            self.session_end = now()
            self.log_session()
            self.submit_logs()

    def terminate(self):
        raise TerminateSession()
    
    def rerun(self):
        if not self.task_test:
            return
        print(colored(f'Checking: {self.task_test.name}', 'blue'))
        self.task_test.run(force=True)
        if self.task_test.status == TaskStatus.PASSED:
            print(colored(
                f'{self.task_test.name} is passing now! Good job! '
                f'Do not hesitate to ask me for help again!',
                'green'
            ))
            raise TerminateSession()
        if self.task_test.error:
            print(colored(self.task_test.error_msg, 'red'))
        raise RestartSession()

    def log_session(self):
        try:
            with gzip.open(
                LOG_DIR / f'delphi_{self.session_id}.json.gz',
                'wt',
                encoding='utf-8'
            ) as f:
                json.dump({
                    'engagement': self.engagement_id,
                    'session': self.session_id,
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
        logs = glob(str(LOG_DIR / 'delphi_*.json*'))
        log_by_id = {}
        for log in logs:
            mtch = self.LOG_RGX.match(log)
            if mtch:
                log_by_id[(mtch.groupdict()['id'], mtch.groupdict()['session'])] = {
                    'path': LOG_DIR / log,
                    'ext': mtch.groupdict().get('ext')
                }
        
        ids = list(log_by_id.keys())

        # todo get whichever sessions have not been recorded and submit them


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
    task: Optional[str] = typer.Argument(
        None,
        help="The gateway task you need help with."
    ),
    llm: LLMBackends = LLMBackends.OPEN_AI.value
):
    global _explicitly_invoked
    _explicitly_invoked = True
    """I need some help! Wake Delphi up!"""
    with delphi_context():
        try:
            tutor().init(task)
        except ConfigurationError as err:
            print(colored(str(err), 'red'))


def main():
    typer.run(delphi)
