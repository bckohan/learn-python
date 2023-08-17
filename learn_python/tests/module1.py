import io
from contextlib import redirect_stdout
import subprocess


def test_hello_world():

    f = io.StringIO()
    with redirect_stdout(f):
        from learn_python.module1 import gateway1

    assert f.getvalue().splitlines() == [
        'imported 1',
        'imported 2',
        'imported 3'
    ]

    # run the hello_world script as a subprocess and capture the output
    output = subprocess.check_output(['python', 'learn_python/module1/hello_world.py'])

