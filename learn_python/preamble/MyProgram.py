"""
This program is roughly equivalent
to MyProgram.c
"""

import sys

def bar():
    return 'bar'

# this is the entry point for a
# python program
if __name__ == '__main__':

    # the command line args
    print(sys.argv)
    print(bar())
