import io
from contextlib import redirect_stdout
import subprocess
from pathlib import Path
import re
import pytest


modules = Path(__file__).parent.parent 
gateway1 = modules / 'module1' / 'gateway1.py'

@pytest.mark.skipif(not gateway1.exists(), reason="Gateway1 exercise does not exist.")
def test_gateway1_part1():

    f = io.StringIO()
    with redirect_stdout(f):
        from learn_python.module1 import gateway1

    lines = f.getvalue().splitlines()
    assert lines[0].strip().lower() == 'print 1', 'Line 1 should be "print 1"'
    assert lines[1].strip().lower() == 'print 2', 'Line 2 should be "print 2"'
    assert lines[2].strip().lower() == 'print 3', 'Line 3 should be "print 3"'


@pytest.mark.skipif(not gateway1.exists(), reason="Gateway1 exercise does not exist.")
def test_gateway1_part2():
    # run the gateway1 script as a subprocess and capture the output
    output = subprocess.check_output(['python', gateway1.absolute()])

    lines = output.decode('utf-8').splitlines()
    assert lines[0].strip().lower() == 'print 1', 'Line 1 should be "print 1"'
    assert lines[1].strip().lower() == 'hello world! python will look for code in these directories:'
    
    # we use regular expressions to check the pretty printed output of the python path list. We also check
    # that the directories exist - because they should!
    
    # check that sys path is a list of paths - luckily we can stitch the pretty printed terminal output
    # back together into a valid python list and evaluate it as code!
    try:
        paths = eval('\n'.join(lines[2:-1]))
        for path in paths:
            assert Path(path).exists() or path.endswith('.zip'), f'{path} is not a valid path'
        assert len(path) > 0, 'sys.path should not be empty'
    except Exception as e:
        pytest.fail(f'Lines 2 through {len(lines)-1} are not a list of paths:\n{e}')
    
    assert lines[-1].strip().lower() == 'print 3', 'Last line should be "print 3"'
