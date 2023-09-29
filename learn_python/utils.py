from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
import warnings
import os
import shutil
import gzip
from pathlib import Path
import re
from os import PathLike
import subprocess
import json
from datetime import datetime
import logging
from logging.handlers import TimedRotatingFileHandler
from dateutil import parser as date_parser


ROOT_DIR = Path(__file__).parent.parent
LOG_DIR = ROOT_DIR / 'logs'

# todo move config into a file
GITHUB_ROOT = Path('https://github.com/bckohan/learn-python')

LOG_DATE_RGX = re.compile(r'(?P<date>(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2}))')


lp_logger = logging.getLogger('learn_python')


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


class GzipRotatingFileHandler(TimedRotatingFileHandler):

    def rotate(self, source, dest):
        if os.path.exists(source):
            os.rename(source, dest)
            subprocess.Popen(['gzip', dest])


def localize_identifier(identifier):
    parts = identifier.split('::')
    return f'{Path(parts[0]).relative_to(ROOT_DIR)}::{parts[1]}'


def strip_colors(s):
    return re.sub(r'\x1B[@-_][0-?]*[ -/]*[@-~]', '', s)


def get_log_date(log_path):
    if log_path:
        match = LOG_DATE_RGX.search(str(log_path))
        if match:
            try:
                return date_parser.parse(match.group('date')).date()
            except date_parser.ParserError:
                pass


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


def git_push_file(file: PathLike) -> bool:
    """
    If the given file has differences from the origin/main branch, 
    commit and push the file.

    This does the following sequence of commands::

        git reset
        git add file.txt
        git commit -m "learn_python.utils.git_push_file()"
        git push origin main
    """

    for command in [
        ('git', 'reset'),
        ('git', 'add', str(file)),
        ('git', 'commit', '-m', 'learn_python.utils.git_push_file()'),
        ('git', 'push')
    ]:
        lp_logger.info('Running: %s', ' '.join(command))
        output = subprocess.run(command, capture_output=True, text=True).stdout.strip()
        if output:
            lp_logger.info('\n\t%s', '\n\t'.join(output.split('\n')))


_logging_configured = False
def configure_logging(level=logging.INFO):
    global _logging_configured
    if not _logging_configured:
        logging.basicConfig()
        os.makedirs(LOG_DIR, exist_ok=True)
        file_handler = GzipRotatingFileHandler(
            str(LOG_DIR / f'learn_python.log'),
            when='midnight',
            backupCount=0,  # never delete old logs
        )
        formatter = logging.Formatter('%(asctime)s - %(name)s - [%(levelno)s]%(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        file_handler.setLevel(level)
        root_logger = logging.getLogger()
        root_logger.setLevel(level)
        root_logger.handlers = [
            *[
                handler for handler in root_logger.handlers
                if not isinstance(handler, logging.StreamHandler)
            ],
            file_handler
        ]
        lp_logger.addHandler(file_handler)
        lp_logger.setLevel(level)
        lp_logger.propagate = False
        test_logger = logging.getLogger('testing')
        test_handler = GzipRotatingFileHandler(
            str(LOG_DIR / f'testing.log'),
            when='midnight',
            backupCount=0,  # never delete old logs
        )
        test_handler.setFormatter(formatter)
        test_handler.setLevel(level)
        test_logger.addHandler(test_handler)
        test_logger.setLevel(level)
        test_logger.propagate = False

    _logging_configured = True


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super(DateTimeEncoder, self).default(obj)