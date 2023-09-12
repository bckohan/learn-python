import sys
from pprint import pprint

print('print 1')
if __name__ == '__main__':
    print('Hello World! Python will look for code in these directories:')
    pprint(sys.path)
else:
    print('print 2')
print('print 3')
