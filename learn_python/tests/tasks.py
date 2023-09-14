from os import PathLike
from enum import IntEnum
import pytest
from pathlib import Path
import sys
from warnings import warn
from typing import Optional, Union
from types import FunctionType
import inspect
from io import StringIO
import contextlib


PACKAGE_DIR = Path(__file__).parent.parent.parent

running_task = None


class TaskStatus(IntEnum):
    """
    The test states a task can be in.
    """

    NOT_RUN = 0
    PASSED = 1
    SKIPPED = 2
    FAILED = 3
    ERROR = 4

    @property
    def css(self):
        return self.name.lower().replace('_', '-')


class Task:
    """
    A data structure holding pertinent information about gateway tasks. Methods
    are provided that help run the task as well.

    :param number: number of the task
    :param name: name of the task
    :param path: the path to the file on disk holding the source code
    :param function: the function if the task is a function, else None. 
        If the function is not yet implemented it will be the string name
        of the function instead of the function itself
    :param test: import string of the function test
    :param module: the module the task is a part of
    :param status: the status of the task/if it has been run during the current
        invocation cycle
    """

    number: int
    name: str
    path: PathLike[str]
    function: Optional[Union[FunctionType, str]] = None
    test: str
    module: str
    status: TaskStatus = TaskStatus.NOT_RUN
    error: Optional[str] = None

    def __init__(
        self,
        number,
        name,
        path,
        test,
        module,
        status=status,
        function=function
    ):
        self.number = number
        self.name = name
        self.path = path
        self.test = test
        self.module = module
        self.status = status
        self.function = function


    @property
    def identifier(self):
        """The pytest run identifier: <file_path>::function"""
        parts = self.test.split('.')
        test_file, test_func = '/'.join(parts[:-1]), parts[-1]
        return f'{PACKAGE_DIR / test_file}.py::{test_func}'


    def run(self):
        """Run the test for the task"""
        global running_task
        # only run if we have not run already!
        if self.status is TaskStatus.NOT_RUN:
            running_task = self
            out = StringIO()

            with contextlib.redirect_stdout(out):
                exit_code = pytest.main(
                    [self.identifier, '-s'],
                    # register this module as a plugin so our hook will be called
                    plugins=[sys.modules[__name__]]
                )

            running_task = None
            if exit_code not in [pytest.ExitCode.OK, pytest.ExitCode.TESTS_FAILED]:
                warn(f'Unable to run test for task {self.module}::{self.name}: {exit_code}')
                self.status = TaskStatus.ERROR
            
            if self.status == TaskStatus.NOT_RUN:
                warn(f'Task status for {self.module}::{self.name} was not updated after run!')

            if self.status in [TaskStatus.ERROR, TaskStatus.FAILED]:
                self.error = out.getvalue()

    @property
    def implementation(self):
        """The student's code for this task"""
        if isinstance(self.function, str):
            return None
        elif self.function:
            return inspect.getsource(self.function)
        
        source_file = Path(self.path0)
        if source_file.is_file():
            return source_file.read_text()
        return None


def pytest_report_teststatus(report, config):
    """
    This is hook that pytest calls after a test is executed with its outcome.
    """
    global running_task
    if running_task.status == TaskStatus.NOT_RUN:
        if report.outcome == 'passed' and report.when == 'teardown':
            running_task.status = TaskStatus.PASSED
        elif report.outcome == 'failed':
            running_task.status = TaskStatus.FAILED
        elif report.outcome == 'skipped' and report.when == 'setup':
            running_task.status = TaskStatus.SKIPPED
    return None
