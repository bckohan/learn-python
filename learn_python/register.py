import typer
import yaml
from delphi.tutor import LLMBackends
from typing import Optional
from learn_python.utils import ROOT_DIR, Singleton
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.types import PrivateKeyTypes
import subprocess
from functools import cached_property

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

    @property
    def tutor(self):
        return _tutor
    
    @tutor.setter
    def tutor(self, value):
        try:
            self.tutor = LLMBackends(value) if not isinstance(value, LLMBackends) else value
        except ValueError as err:
            warnings.warn(
                f'Unrecognized tutor driver: {conf.get("tutor")}. Defaulting to {self.tutor.value}'
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
            ).stdout
        except Exception:
            pass
        return None
    
    def is_configured(self):
        return PRIVATE_KEY_FILE.exists() and self.registered

    def load_private_key(self):
        if PRIVATE_KEY_FILE.is_file():
            with open(PRIVATE_KEY_FILE, 'rb') as f:
                self.private_key = serialization.load_pem_private_key(
                    f.read(),
                    password=None,
                    backend=default_backend()
                )

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
        try:
            self.tutor = LLMBackends(config.get('tutor', self.tutor.value))
        except ValueError as err:
            warnings.warn(
                f'Unrecognized tutor driver: {config.get("tutor")}. Defaulting to {self.tutor.value}'
            )
        return self
    
    def try_authorize_tutor(self):
        from learn_python.client import CourseClient
        client = CourseClient()
        tutor_backend, tutor_api_key = client.get_tutor_auth()
        if tutor_backend:
            self.tutor = tutor_backend
            if tutor_api_key:
                from learn_python.delphi.tutor import tutor
                tutor(self.tutor).write_key(tutor_api_key)
                typer.echo('Delphi has been authorized!')
                return True
        return False
    
    def write(self):
        with open(self.CONFIG_FILE, 'w') as cfg:
            yaml.dump(self.to_dict(), cfg)
        return True
    
    def register(self, exclusive: bool = False):
        from learn_python.client import CourseClient
        client = CourseClient()

        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = self.private_key.public_key()

        with open(PUBLIC_KEY_FILE, 'w' if exclusive else '+a', encoding='utf-8') as f:
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

        if client.register():
            self.try_authorize_tutor()
            return True
        return False
        

    def sign_message(self, message):
        signature = None
        if self.private_key:
            signature = self.private_key.sign(
                message.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
        return signature


def register(
    force: bool = typer.Option(
        False,
        '-f',
        '--force',
        help='Re-register with the course.'
    ),
    exclusive: bool = typer.Option(
        False,
        '-e',
        '--exclusive',
        help=(
            'Overwrite the existing public key file. If you have any other clones of this '
            'repository, this will unregister them from the course.'
        )
    )
):
    if Config().is_registered() and not force:
        Config().try_authorize_tutor()
    elif Config().register(exclusive=exclusive):
        typer.echo('Your course is now registered!')
        if Config().enrollment is not None:
            typer.echo(f'You have been enrolled in course: {Config().enrollment}')
    else:
        typer.echo(f'Course registration failed. If this is in error, contact your instructor.')


def main():
    typer.run(register)
