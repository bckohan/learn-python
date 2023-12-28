import io
from contextlib import redirect_stdout
import subprocess
from pathlib import Path
import sys
import pytest
from learn_python.tests.tasks import Task


modules = Path(__file__).parent.parent 
gateway1 = modules / 'module1_tools' / 'gateway1.py'

@pytest.mark.skipif(not gateway1.exists(), reason="Gateway1 exercise does not exist.")
def test_gateway1_part1():
    import importlib
    from learn_python.module1_tools import gateway1
    
    f = io.StringIO()
    with redirect_stdout(f):
        # depending on how the tests are called the module may have already
        # been imported - we need to make sure the code inside is executed
        # on import, so we use importlib to reload it
        importlib.reload(gateway1)

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
    
    # check that sys path is a list of paths - luckily we can stitch the pretty printed terminal output
    # back together into a valid python list and evaluate it as code!
    try:
        paths = set(eval('\n'.join(lines[2:-1])))
        assert len(set(sys.path)) - len(paths) < 2 * len(paths), 'pretty printed path list looks wrong'
        assert len(paths) >= 4, 'pretty printed path list does not have enough entries'
    except Exception as e:
        pytest.fail(f'Lines 2 through {len(lines)-1} are not a list of paths:\n{e}')
    
    assert lines[-1].strip().lower() == 'print 3', 'Last line should be "print 3"'


module1_tasks = [
    Task(
        number=1,
        name='part1',
        path=gateway1,
        test='learn_python.tests.module1.test_gateway1_part1',
        module='module1',
        modules=['learn_python.module1_tools.gateway1']
    ),
    Task(
        number=2,
        name='part2',
        path=gateway1,
        test='learn_python.tests.module1.test_gateway1_part1',
        module='module1',
        modules=['learn_python.module1_tools.gateway1']
    )
]
