import logging
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
import warnings
import os
import shutil
import gzip
from pathlib import Path
import re


ROOT_DIR = Path(__file__).parent.parent

# todo move config into a file
GITHUB_ROOT = Path('https://github.com/bckohan/learn-python')


class ConeOfSilence(redirect_stdout, redirect_stderr):
    """
    A context manager that goes through heroic efforts to suppress
    all console output.
    """

    buffer: StringIO

    def __init__(self):
        self.buffer = StringIO()
        redirect_stderr.__init__(self, self.buffer)
        redirect_stdout.__init__(self, self.buffer)

    def __enter__(self):
        redirect_stdout.__enter__(self)
        redirect_stderr.__enter__(self)
        self.backup_filters = warnings.filters.copy()
        warnings.simplefilter("ignore")
        self.loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
        self.original_levels = {logger: logger.level for logger in self.loggers}
        for logger in self.loggers:
            logger.setLevel(666)

    def __exit__(self, exc_type, exc_value, traceback):
        for logger, original_level in self.original_levels.items():
            logger.setLevel(original_level)
        redirect_stdout.__exit__(self, exc_type, exc_value, traceback)
        redirect_stderr.__exit__(self, exc_type, exc_value, traceback)
        warnings.filters = self.backup_filters


class GzipFileHandler(logging.FileHandler):
    """
    A logging file handler that gzips the log file when it is closed.
    """
    def close(self):
        # Call the original close method

        super().close()

        # Gzip the log file
        with open(self.baseFilename, 'rb') as log_file, gzip.open(self.baseFilename + '.gz', 'wb') as gzipped_log:
            shutil.copyfileobj(log_file, gzipped_log)

        os.remove(self.baseFilename)


def localize_identifier(identifier):
    parts = identifier.split('::')
    return f'{Path(parts[0]).relative_to(ROOT_DIR)}::{parts[1]}'


def strip_colors(s):
    return re.sub(r'\x1B[@-_][0-?]*[ -/]*[@-~]', '', s)


class _Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    @classmethod
    def is_instantiated(cls, typ):
        return typ in cls._instances

    @classmethod
    def destroy(cls, typ):
        if typ in cls._instances:
            del cls._instances[typ]


class Singleton(_Singleton('SingletonMeta', (object,), {})):
    """
    Inherit from this class first, to make an object a singleton. The object can be accessed anywhere
    using YourObject( ).instance_function( ). If initialization with a configuration is attempted more
    than once an exception is thrown.
    """
