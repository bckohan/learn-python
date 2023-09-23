import typer
import yaml
from learn_python.delphi.tutor import LLMBackends
from typing import Optional
from learn_python.utils import ROOT_DIR, Singleton, git_push_file
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.types import (
    PrivateKeyTypes,
    PublicKeyTypes
)
from cryptography.exceptions import InvalidSignature
import subprocess
from functools import cached_property
from requests import HTTPError
from termcolor import colored
from learn_python import main
import time
import re
import warnings


PRIVATE_KEY_FILE = ROOT_DIR / '.private_key.pem'
PUBLIC_KEY_FILE = ROOT_DIR / 'public_keys.pem'


class Config(Singleton):

    CONFIG_FILE = ROOT_DIR / '.config.yaml'

    server: Optional[str] = None
    enrollment: Optional[str] = None
    registered: bool = False
    _tutor: LLMBackends = LLMBackends.OPEN_AI

    private_key: Optional[PrivateKeyTypes] = None
    public_keys: Optional[PublicKeyTypes] = None

    @property
    def tutor(self):
        return self._tutor
    
    @tutor.setter
    def tutor(self, value):
        try:
            if value is not None:
                self._tutor = LLMBackends(value) if not isinstance(value, LLMBackends) else value
        except ValueError as err:
            warnings.warn(
                f'Unrecognized tutor driver: {value}. Defaulting to {self.tutor.value}'
            )

    def __init__(self):
        if self.CONFIG_FILE.is_file():
            with open(self.CONFIG_FILE, 'r') as cfg:
                conf = yaml.safe_load(cfg)
                self.server = conf.get('server', self.server)
                self.registered = conf.get('registered', self.registered)
                self.enrollment = conf.get('enrollment', self.enrollment)
                self.tutor = conf.get('tutor', self.tutor)
        self.load_private_key()

    @cached_property
    def origin(self):
        """The forked github repository - this will be used as the unique ID for the student"""
        try:
            return subprocess.run(
                ['git', 'remote', 'get-url', 'origin'],
                capture_output=True,
                text=True
            ).stdout.strip()
        except Exception:
            pass
        return None
    
    def is_registered(self):
        return PRIVATE_KEY_FILE.exists() and self.registered

    def load_private_key(self):
        if PRIVATE_KEY_FILE.is_file():
            with open(PRIVATE_KEY_FILE, 'rb') as f:
                contents = f.read()
                if contents:
                    self.private_key = serialization.load_pem_private_key(
                        contents,
                        password=None,
                        backend=default_backend()
                    )
        return self.private_key

    def load_public_keys(self):
        self.public_keys = []
        if PUBLIC_KEY_FILE.is_file():
            with open(PUBLIC_KEY_FILE, 'rb') as f:
                pem_data = f.read().decode()
            
            # Splitting the keys based on PEM headers/footers
            pem_keys = [
                f"-----BEGIN {m[1]}-----{m[2]}-----END {m[1]}-----"
                for m in re.findall(
                    r"(-----BEGIN (.*?)-----)(.*?)(-----END \2-----)",
                    pem_data,
                    re.S
                )
            ]

            self.public_keys = [
                serialization.load_pem_public_key(
                    pem.encode(),
                    backend=default_backend()
                ) for pem in pem_keys
            ]
        return self.public_keys

    def to_dict(self):
        return {
            'server': self.server,
            'registered': self.registered,
            'enrollment': self.enrollment,
            'tutor': self.tutor.value
        }
    
    def update(self, config: dict):
        self.server = config.get('server', self.server)
        self.registered = config.get('registered', self.registered)
        self.enrollment = config.get('enrollment', self.enrollment)
        self.tutor = config.get('tutor', self.tutor)
        return self

    def try_authorize_tutor(self):
        from learn_python.client import CourseClient
        client = CourseClient()
        tutor_auth = client.get_tutor_auth() or {}
        if 'tutor' in tutor_auth:
            self.tutor = tutor_auth['tutor']
            if 'secret' in tutor_auth:
                from learn_python.delphi.tutor import tutor
                tutor(self.tutor).write_key(tutor_auth['secret'])
                typer.echo('Delphi has been authorized!')
                return True
        return False
    
    def write(self):
        with open(self.CONFIG_FILE, 'w') as cfg:
            yaml.dump(self.to_dict(), cfg)
        return True
    
    def keys_valid(self):
        self.load_private_key()
        self.load_public_keys()
        if not (self.public_keys and self.private_key):
            return False
        
        def verify(key):
            msg = str(int(time.time())).encode()
            try:
                key.verify(
                    self.sign_message(msg),
                    msg,
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    hashes.SHA256()
                )
                return True
            except InvalidSignature:
                return False
        return any((verify(key) for key in self.public_keys))

    def register(self, reset: bool = False):
        from learn_python.client import CourseClient
        client = CourseClient()

        if reset or not self.keys_valid():
            self.private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
            )
            public_key = self.private_key.public_key()

            with open(PUBLIC_KEY_FILE, 'w' if reset else '+a', encoding='utf-8') as f:
                f.write(public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                ).decode('utf-8'))
            
            with open(PRIVATE_KEY_FILE, 'wb') as f:
                f.write(
                    self.private_key.private_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PrivateFormat.TraditionalOpenSSL,
                        encryption_algorithm=serialization.NoEncryption()
                    )
                )
        if not self.keys_valid():
            raise RuntimeError(
                'Unable to generate functioning key/value pair.'
            )
        
        git_push_file(PUBLIC_KEY_FILE)

        try:
            client.register()
        except HTTPError as err:
            return False
        
        try:
            self.try_authorize_tutor()
        except HTTPError as err:
            pass
        return True

    def sign_message(self, message: str | bytes):
        signature = None
        if self.private_key:
            signature = self.private_key.sign(
                message.encode() if isinstance(message, str) else message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
        return signature

@main(catch=True)
def register(
    force: bool = typer.Option(
        False,
        '-f',
        '--force',
        help='Re-register with the course.'
    ),
    reset: bool = typer.Option(
        False,
        '--reset',
        help=(
            'Overwrite the existing public key file. If you have any other clones of this '
            'repository, this will unregister them from the course.'
        )
    )
):
    if Config().is_registered() and not force:
        Config().try_authorize_tutor()
    elif Config().register(reset=reset):
        typer.echo(colored('Your course is now registered!', 'green'))
        if Config().enrollment is not None:
            typer.echo(colored(f'You have been enrolled in course: {Config().enrollment}'), 'green')
    else:
        typer.echo(
            colored('Course registration failed. If this is in error, contact your instructor.', 'red')
        )