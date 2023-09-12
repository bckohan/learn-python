from learn_python.tests.module1 import *
from learn_python.tests.module2 import *
from copy import copy
from docutils.transforms import universal

tasks = {}

for name, attr in copy(globals()).items():
    # build our tasks mapping
    # tasks = { module_name: { task_name: task }, etc}
    # modules and tasks should iterate in order
    if name.startswith('module') and name.endswith('_tasks'):
        tasks[name.split('_')[0]] = {
            task.name: task for task in sorted(attr, key=lambda x: x.number)
        }
