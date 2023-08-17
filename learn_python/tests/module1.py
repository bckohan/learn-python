import io
from contextlib import redirect_stdout
import subprocess
from pathlib import Path
import re

modules = Path(__file__).parent.parent 
gateway1 = modules / 'module1' / 'gateway1.py'


def test_gateway1_part1():

    f = io.StringIO()
    with redirect_stdout(f):
        from learn_python.module1 import gateway1

    lines = f.getvalue().splitlines()
    assert lines[0].strip().lower() == 'print 1', 'Line 1 should be "print 1"'
    assert lines[1].strip().lower() == 'print 2', 'Line 2 should be "print 2"'
    assert lines[2].strip().lower() == 'print 3', 'Line 3 should be "print 3"'


def test_gateway1_part2():
    # run the gateway1 script as a subprocess and capture the output
    output = subprocess.check_output(['python', gateway1.absolute()])

    lines = output.decode('utf-8').splitlines()
    assert lines[0].strip().lower() == 'print 1', 'Line 1 should be "print 1"'
    assert lines[1].strip().lower() == 'hello world! python will look for code in these directories:'
    
    # we use regular expressions to check the pretty printed output of the python path list. We also check
    # that the directories exist - because they should!
    
    # first path line
    mtch = re.match(r"\['((\/[^/,']*)+)',", lines[2].strip())
    assert mtch and Path(mtch.groups()[0]).exists(), f'Line 3 should be the first path in sys.path'
    
    # lines in the middle
    for idx, line in enumerate(lines[3:-2]):
        mtch = re.match(r"'((\/[^/,']*)+)',", line.strip())
        assert mtch and (Path(mtch.groups()[0]).exists() or mtch.groups()[0].endswith('.zip')), f'Line {idx+4} should be a valid path in sys.path'
    
    # last path line
    mtch = re.match(r"'((\/[^/,']*)+)'\]", lines[-2].strip())
    assert mtch and Path(mtch.groups()[0]).exists(), f'Line {len(lines)-1} should be the last path in sys.path'
    
    assert lines[-1].strip().lower() == 'print 3', 'Last line should be "print 3"'
