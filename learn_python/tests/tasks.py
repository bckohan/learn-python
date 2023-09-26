from os import PathLike
from enum import IntEnum
import pytest
from pathlib import Path
import sys
from warnings import warn
from typing import Optional, Union, List
from types import FunctionType, ModuleType
import inspect
from contextlib import redirect_stdout
from io import StringIO
from learn_python.tests.utils import import_string
import importlib
import contextlib
import re
import io


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
    modules: Optional[List[Union[ModuleType, str]]] = None
    test: str
    module: str
    status: TaskStatus = TaskStatus.NOT_RUN
    error: Optional[str] = None
    timeout: int = 5

    ERROR_MSG_RGX = re.compile('^E\s+AssertionError[:]\s+(?P<msg>.+)\n\n', re.M)
    MODULE_NUM_RGX = re.compile(r'module(?P<num>\d+)')

    def __init__(
        self,
        number,
        name,
        path,
        test,
        module,
        status=status,
        function=function,
        modules=modules,
        timeout=timeout
    ):
        self.number = number
        self.name = name
        self.path = path
        self.test = test
        self.module = module
        self.status = status
        self.function = function
        self.modules = modules
        self.timeout = timeout

        f = io.StringIO()
        with redirect_stdout(f):  # silence!
            for idx, mod in enumerate(self.modules):
                if isinstance(mod, str):
                    try:
                        self.modules[idx] = importlib.import_module(mod)
                    except Exception:
                        pass

    @property
    def identifier(self):
        """The pytest run identifier: <file_path>::function"""
        parts = self.test.split('.')
        test_file, test_func = '/'.join(parts[:-1]), parts[-1]
        return f'{PACKAGE_DIR / test_file}.py::{test_func}'
    
    @property
    def module_number(self):
        if self.module:
            mtch = self.MODULE_NUM_RGX.search(self.module)
            if mtch:
                return int(mtch.groupdict()['num'])
            return None

    @property
    def error_msg(self):
        """The short, specific error reported by the test"""
        if self.error:
            mtch = self.ERROR_MSG_RGX.search(self.error, re.M)
            if mtch:
                return mtch.groupdict()['msg']
        return None

    def run(self, force=False):
        """
        Run the test for the task. If the test was previously run it will not
        run again unless force is set to true.
        """
        global running_task

        # only run if we have not run already, unless we are forced!
        if force and self.status is not TaskStatus.NOT_RUN:
            # force reload of code from disk, this is likely happening as part
            # of a tutor workflow
            f = io.StringIO()
            with redirect_stdout(f):  # silence!
                for idx, mod in enumerate(self.modules):
                    try:
                        if isinstance(mod, str):
                            self.modules[idx] = importlib.import_module(mod)
                        else:
                            self.modules[idx] = importlib.reload(mod)

                        # todo - need a more formal assignment structure, perhaps utilizing ast?
                        # this kinda thing is fairly brittle
                        func_name = self.function if isinstance(self.function, str) else self.function.__name__
                        func_reload = getattr(self.modules[idx], func_name, None)
                        if func_reload and isinstance(func_reload, FunctionType):
                            self.function = func_reload

                        # we also need to reload the test because its imports may be stale
                        importlib.reload(inspect.getmodule(import_string(self.test)))
                    except Exception:
                        pass
            self.status = TaskStatus.NOT_RUN
            self.error = None

        if self.status is TaskStatus.NOT_RUN:
            running_task = self

            out = StringIO()
            with contextlib.redirect_stdout(out):
                exit_code = pytest.main(
                    [f'--timeout={self.timeout}', self.identifier, '-s'],
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
        """The student's code for this task - todo this will need to be enhanced for more complex tasks"""
        if isinstance(self.function, str):
            return None
        elif self.function:
            return inspect.getsource(self.function)
        
        source_file = Path(self.path)
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
