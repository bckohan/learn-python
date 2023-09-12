from pathlib import Path
import os
import typer
from contextlib import contextmanager
from learn_python.tests.tests import tasks as task_tests
from learn_python.tests.tasks import TaskStatus
import re
from functools import cached_property
from sphinx.application import Sphinx
from docutils.nodes import (
    section,
    GenericNodeVisitor,
    SkipChildren,
    Admonition,
    paragraph
)
from os import PathLike
from termcolor import colored
from sphinx.ext.todo import Todo
from sphinx.addnodes import desc


_mapper = None


def task_map():
    global _mapper
    if _mapper is None:
        _mapper = TaskMapper()
        _mapper.build()
    return _mapper


def setup(app):
    global _mapper
    if not _mapper:
        # if the mapper already exists we're not hooking into a documentation build
        # process, therefore we shouldn't register our event callback because the
        # doctree has already been built externally
        _mapper = TaskMapper()
        app.connect('doctree-resolved', _mapper.process_doctree)


DOC_DIR = Path(__file__).parent.parent / 'docs'
DOC_SRC_DIR = DOC_DIR / 'source'
DOC_BLD_DIR = DOC_DIR / 'build'


app = typer.Typer()
doc_dir = Path(__file__).parent.parent / 'docs'


class DocError(Exception):
    pass


# build section to task mapping
class TaskMapper:
    """
    A utility class that is responsible for mapping sections in the documentation to 
    their corresponding gateway tasks and tests. This class is used to build the mapping
    and then to query it.
    """

    MODULE_RGX = re.compile('(?P<module>module\d+)')

    tasks: dict
    task_sections: dict

    test_status = None

    def __init__(self):
        self.tasks = {}
        self.task_sections = {}

    class AssignmentDocs:
        """
        Structured data for each task holding pointers into the documentation tree.

        Task docs must be of the following format:

        task_name
        =========

        .. todo::

            A single todo statement describing the high level assignment.

        .. admonition:: Requirement

            A single paragraph requirement statement or a list of requirements. These
            are additional requirements levied on the task beyond functionality that
            are required for it to pass. Usually referring to implementation details
            like: the solution can only be a single statement.
        
        .. hint:: 

            A single paragraph hint, or a list of hints. These are meant to point the
            student in the right direction.

        In addition to the high level documentation, there may be docstring stubs for
        functions and classes. These will be parsed out as well and stored in the
        docstrings list.
        """
        name: str
        node: section
        gateway_node: section
        source: PathLike
        gateway_source: PathLike

        todo: str
        requirements: list
        hints: list

        autodoc_nodes: list

        def __init__(
            self,
            name,
            node,
            gateway_node,
            source,
            gateway_source
        ):
            self.name = name
            self.node = node
            self.gateway_node = gateway_node
            self.source = source
            self.gateway_source = gateway_source

            self.requirements = []
            self.hints = []

            def parse_admonition(admonition):
                parts = []
                for node in admonition.traverse():
                    if isinstance(node, paragraph):
                        parts.append(node.astext())
                return parts

            todos = []
            for node in self.node.traverse(Admonition):
                # Here, you can extract information from the Admonition node as needed
                # For simplicity, we'll just extract the text
                if node.tagname == 'hint':
                    self.hints.extend(parse_admonition(node))
                elif node.tagname == 'todo' or isinstance(node, Todo.node_class):
                    todos.extend(parse_admonition(node))
                elif node.tagname == 'admonition':
                    if node.next_node().astext().lower() == 'requirement':
                        self.requirements.extend(parse_admonition(node))

            self.todo = '\n'.join(todos)

            self.autodoc_nodes = [node for node in self.node.traverse(desc)]


    class AssignmentCollector(GenericNodeVisitor):

        assignments = None

        gateway_section = None
        assignment_section = None

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.assignments = {}
            self.tasks = {}

        def default_visit(self, node):
            """Base class requires that this be implemented - but we don't need to do anything"""

        def default_departure(self, node):
            """Base class requires that this be implemented - but we don't need to do anything"""

        def visit_section(self, node):
            if not isinstance(node, section):
                return
            if not self.gateway_section and 'gateway' in node[0].astext().lower():
                self.gateway_section = node
            elif self.gateway_section and not self.assignment_section:
                name = node[0].astext().rstrip('()').lower().replace(' ', '')
                self.assignments[name] = TaskMapper.AssignmentDocs(
                    name=name,
                    node=node,
                    gateway_node=self.gateway_section,
                    source=node.source,
                    gateway_source=self.gateway_section.source
                )
                self.assignment_section = node
                raise SkipChildren()  # no need to traverse into the task section

        def depart_section(self, node):
            if node is self.gateway_section:
                self.gateway_section = False
            elif node is self.assignment_section:
                self.assignment_section = None


    def build(self):
        """
        Build the doctree and parse out the tasks. If this is called we're not
        running our task mapper as part of a documentation build process, so we
        avoid editing the doctree. This might happen as part of our tutor execution
        flow for example, where we need access to the structured data from the
        docs but aren't building them.
        """
        self.task_sections.clear()
        self.tasks.clear()
        self.app.build()
        for doc_name in self.app.env.found_docs:
            self.read_tasks(
                self.app.env.get_doctree(doc_name),
                doc_name
            )

    def process_doctree(self, app, tree, doc_name):
        """
        This is the callback registered to hook into the documentation build
        process. This means we need to edit our doctree with the results of the
        test runs because the documentation is being written!
        """
        module, tasks = self.read_tasks(tree, doc_name)

        for task in tasks:
            task_test = self.get_task_test(module, task)
            task_doc = self.get_task_doc(module, task)
            task_test.run()
            if task_test.status is TaskStatus.PASSED:
                task_doc.node.attributes.setdefault('classes', []).append('passed')
            elif task_test.status is TaskStatus.FAILED:
                task_doc.node.attributes.setdefault('classes', []).append('failed')


    def read_tasks(self, tree, doc_name):
        """
        Run the assignment collector on the document to find any gateway tasks and
        parse them out into AssignmentDoc objects.
        """
        mtch = self.MODULE_RGX.search(doc_name)
        if mtch:
            # gateway tasks must belong to a module
            module = mtch.groupdict()['module']
            visitor = self.AssignmentCollector(tree)
            tree.walkabout(visitor)
            if visitor.assignments:
                self.task_sections.setdefault(module.lower(), {})
                self.task_sections[module.lower()].update(visitor.assignments)
                return module, visitor.assignments
            return module, []
        return None, []

    def check(self):
        """
        Check that the gateway tasks parsed from our doctree match the gateway tasks
        registered with pytest.
        """
        errors = []
        t_diff = set(task_tests.keys()) - set(self.task_sections)
        d_diff = set(self.task_sections.keys()) - set(task_tests.keys())

        def format_diff(diff):
            return '\n\t\t'.join(diff)
        
        if t_diff:
            errors.append(f'Docs are missing the following task modules:\n\t\t{format_diff(t_diff)}.')
        if d_diff:
            errors.append(f'Tests are missing the following task modules:\n\t\t{format_diff(d_diff)}.')

        for module in task_tests.keys():
            test_module = task_tests[module]
            doc_module = self.task_sections.get(module, {})
            t_diff = set(test_module.keys()) - set(doc_module.keys())
            d_diff = set(doc_module.keys()) - set(test_module.keys())
            if t_diff:
                errors.append(f'For {module} docs are missing the following tasks:\n\t\t{format_diff(t_diff)}.')
            if d_diff:
                errors.append(f'For {module} tests are missing the following tasks:\n\t\t{format_diff(d_diff)}.')

        if errors:
            errors = '\n\t'.join(errors)
            raise DocError(
                f'Tests and documentation have the following gateway task mismatches: \n\t'
                f'{errors}'
            )

    def get_task_doc(self, module, task_name):
        return self.task_sections.get(module, {}).get(task_name, None)
    
    def get_task_test(self, module, task_name):
        return task_tests.get(module, {}).get(task_name, None)

    @cached_property
    def app(self):
        """Get a sphinx app for parsing the documentation, that will use our doc's configuration."""
        return Sphinx(
            srcdir=DOC_SRC_DIR,
            confdir=DOC_SRC_DIR,
            outdir=DOC_BLD_DIR,
            doctreedir=DOC_BLD_DIR / 'doctrees',
            buildername='dummy'
        )


@contextmanager
def doc_context():
    assert DOC_DIR.is_dir()
    start_dir = os.getcwd()
    os.chdir(DOC_DIR)
    yield
    os.chdir(start_dir)


@app.command()
def build():
    """Build the documentation - this will always clean it first."""
    clean()
    with doc_context():
        os.system('make html')


@app.command()
def clean():
    """Delete the built documentation."""
    with doc_context():
        os.system('make clean')


@app.command()
def check():
    """Check the documentation for errors."""
    with doc_context():
        status = 0
        try:
            task_map().check()
        except Exception as err:
            status = 1
            print(colored(err, 'red'))

        # todo - also run doc8 or something

    return status


if __name__ == "__main__":
    app()
