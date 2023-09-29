from pathlib import Path
import os
import typer
from contextlib import contextmanager
from learn_python.tests.tests import tasks as task_tests
from learn_python.tests.utils import import_string
from learn_python.tests.tasks import TaskStatus
import re
from functools import cached_property
from sphinx.application import Sphinx
from docutils.nodes import (
    document,
    section,
    GenericNodeVisitor,
    SkipChildren,
    Admonition,
    paragraph,
    title,
    Text,
    reference,
    list_item,
    literal_block
)
from os import PathLike
from termcolor import colored
from sphinx.ext.todo import Todo
from sphinx.addnodes import desc, pending_xref
from typing import List, Dict, Union, Optional, Tuple
from types import FunctionType, ModuleType
from enum import Enum, auto
from warnings import warn
import inspect
from learn_python.utils import ROOT_DIR, GITHUB_ROOT
from docutils.parsers.rst import Directive
import json
from learn_python.utils import ConeOfSilence, configure_logging

_mapper = None
DETACHED_DEFAULT = False


CODE_REF_RE = re.compile(r'(?:(?P<name>.+)\s*\<(?P<link1>[^>.]+)[.](?P<ext1>.+)\>)|(?:(?P<link2>[^>.]+)[.](?P<ext2>.+))')


def code_ref_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """
    This code ref generates a vscode open link when built locally and a github code link when
    built in detached mode.

    Usage::

        :code-ref:`file_name <path/to/file.py>`
    
    """
    env = inliner.document.settings.env
    match = CODE_REF_RE.match(text)
    if not match:
        raise Directive.error(
            msg=f'{text} is not a valid code-ref. Should be: "link_name <path/to/file.py>"'
        )
    match = match.groupdict()
    if match['link1']:
        pth = Path(f"{match['link1']}.{match['ext1']}")
        name = match['name']
    else:
        pth = Path(f"{match['link2']}.{match['ext2']}")
        name = pth.name

    node = reference('', '', internal=False)
    if env.config.detached:
        node['refuri'] = str(GITHUB_ROOT / 'blob/main' / pth)
    else:
        node['refuri'] = f'vscode://file/{ROOT_DIR / pth}'
    node['reftitle'] = name.strip()
    node += Text(name)
    return [node], []


def task_map():
    global _mapper
    if _mapper is None:
        _mapper = TaskMapper()
        _mapper.build()
    return _mapper


def setup(app):
    global _mapper
    global DETACHED_DEFAULT
    from learn_python.register import lock_reporting
    # lots of tests are run individually during doc build - this avoids reporting 
    # after each one!
    lock_reporting()
    app.add_config_value('detached', DETACHED_DEFAULT, 'env', types=[bool])
    app.add_role('code-ref', code_ref_role)
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


class DocError(Exception):
    pass


class NodeType(Enum):

    FUNCTION = auto()
    CLASS = auto()
    MODULE = auto()


class AutodocTree(GenericNodeVisitor):

    class AutodocNode:

        name: str
        object: Union[ModuleType, FunctionType, type]
        node: desc
        node_type: NodeType

        children: list

        def __init__(self, name, object, node, node_type):
            self.name = name
            self.object = object
            self.node = node
            self.node_type = node_type

            self.children = []

        def append(self, node):
            self.children.append(node)

        @property
        def docstring(self):
            return getattr(self.object, '__doc__', '')
        
        @property
        def file(self):
            return Path(inspect.getfile(self.object))


    root_nodes: list[AutodocNode]
    stack: list[desc]

    class_re = re.compile('^class (?P<import_string>[\w.]+)')
    function_re = re.compile('^(?P<import_string>[\w.]+)[(]{1}')
    module_re = re.compile('^(?P<import_string>[\w.]+)')  # todo

    def __bool__(self):
        return bool(self.root_nodes)

    def __init__(self):
        self.root_nodes = []

    def default_visit(self, node):
        if isinstance(node, desc):
            # what is this? - string name matching seems brittle, but
            # the doctree does not appear to save references to the python constructs
            # so we have to do it this way
            match = self.class_re.search(node[0].astext())
            node_type = None
            import_str = ''
            if match:
                import_str = match.groupdict()['import_string']
                node_type = NodeType.CLASS
            else:
                match = self.function_re.search(node[0].astext())
                if match:
                    import_str = match.groupdict()['import_string']
                    node_type = NodeType.FUNCTION
                else:
                    match = self.module_re.search(node[0].astext())
                    if match:
                        import_str = match.groupdict()['import_string']
                        node_type = NodeType.MODULE
            
            if not import_str or node_type is None:
                warn(f'Unable to resolve autodoc node: {node[0].astext()}')
                raise SkipChildren()
            
            parent = self.stack[-1] if self.stack else None
            if parent:
                obj = getattr(parent.object, import_str, None)
            else:
                obj = import_string(import_str)
            if obj is None:
                warn(f'Unable to resolve autodoc node: {import_str}')
                raise SkipChildren()

            tree_node = self.AutodocNode(
                name=import_str.split('.')[-1],
                object=obj,
                node=node,
                node_type=node_type
            )
            if self.stack:
                # if we've got a node on the stack, record this new one as its child
                self.stack[-1].append(tree_node)
            else:
                self.root_nodes.append(tree_node)
            self.stack.append(tree_node)

    def default_departure(self, node):
        if self.stack and self.stack[-1].node is node:
            self.stack.pop()

    # no reason to fail on unknown nodes
    def unknown_visit(self, node):
        pass
    
    def unknown_departure(self, node):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root_nodes = []
        self.stack = []


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

    _app: Optional[Sphinx] = None

    # the toctree gateway assignment hierarchy
    hierarchy = None
    
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

        # the functions that are autodoc-ed
        functions: List[FunctionType]

        # the modules that are autodoc-ed
        modules: List[ModuleType]

        # the classes that are autodoc-ed, and their methods
        # and subclasses that are as well
        classes: Dict[type, List[Union[type, FunctionType]]]

        # the autodoc tree 
        autodoc: AutodocTree

        # other tasks that are dependencies
        dependencies: List[Tuple[str, str]]

        def __init__(
            self,
            name,
            node,
            gateway_node,
            source,
            gateway_source,
            document
        ):
            self.name = name
            self.node = node
            self.gateway_node = gateway_node
            self.source = source
            self.gateway_source = gateway_source
            self.dependencies = []

            self.requirements = []
            self.hints = []

            def find_dependencies(node):
                replacements = {}
                for ref in node.traverse(lambda x: isinstance(x, (reference, pending_xref))):
                    target = 'refid' if 'refid' in ref else 'reftarget'
                    ref_id = ref.get(target, '')
                    if ref_id.startswith('module'):
                        parts = ref_id.split('-')
                        if len(parts) > 1:
                            module = parts[0]
                            task_name = '_'.join(parts[1:])
                            self.dependencies.append((module, task_name))
                            replacements[ref_id] = task_name
                return replacements
            
            def parse_admonition(admonition):
                parts = []
                replacements = find_dependencies(admonition)
                for node in admonition.traverse():
                    if isinstance(node, paragraph):
                        parts.append(node.astext())
                for ref, task_name in replacements.items():
                    for idx, part in enumerate(parts):
                        parts[idx] = part.replace(ref, task_name)
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

            self.autodoc = AutodocTree(document)
            self.node.walkabout(self.autodoc)


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

        # no reason to fail on unknown nodes
        def unknown_visit(self, node):
            pass
        
        def unknown_departure(self, node):
            pass

        def visit_section(self, node):
            if not isinstance(node, section):
                return
            if not self.gateway_section and 'gateway' in node[0].astext().lower():
                self.gateway_section = node
            elif self.gateway_section and not self.assignment_section:
                name = node[0].astext()
                if '()' in name:
                    name = name[:name.index('()')]
                name = name.lower().replace(' ', '')
                self.assignments[name] = TaskMapper.AssignmentDocs(
                    name=name,
                    node=node,
                    gateway_node=self.gateway_section,
                    source=node.source,
                    gateway_source=self.gateway_section.source,
                    document=self.document
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

        This function adds a bunch of information about the student's task code
        into the doctree, including errors if there are any.
        """
        self.process_toctree(app)  # all toctrees will be processed on the first doc
        module, tasks = self.read_tasks(tree, doc_name)

        for task in tasks:
            task_test = self.get_task_test(module, task)
            task_doc = self.get_task_doc(module, task)
            task_test.run()
            task_doc.node['classes'].extend(['task', task_test.status.css])

            if task_test.error:
                err_section = section(ids=[f'{task_test.name}-error'])
                err_section['classes'].append('error-output')
                title_text = 'Error'
                err_msg = task_test.error_msg
                if err_msg:
                    title_text += f': {err_msg}'
                title_node = title(title_text, title_text)
                err_section += title_node
                para_text = task_test.error
                para_node = literal_block(para_text, para_text)
                err_section += para_node
                task_doc.node += err_section
                
            if task_test.implementation:
                impl_section = section(ids=[f'{task_test.name}-implementation'])
                impl_section['classes'].append('task-implementation')
                title_text = 'Implementation'
                title_node = title(title_text, title_text)
                impl_section += title_node
                para_text = task_test.implementation
                para_node = literal_block(para_text, para_text)
                impl_section += para_node
                task_doc.node += impl_section
            
            # change todo's to completed's because we can!
            if task_test.status == TaskStatus.PASSED:
                for todo in task_doc.node.traverse(Todo.node_class):
                    todo[0].children[0] = Text('Completed')

            if 'gateway' not in task_doc.gateway_node['classes']:
                task_doc.gateway_node['classes'].extend(['gateway'])
            
            if not hasattr(task_doc.gateway_node, '_task_status'):
                task_doc.gateway_node._task_status = TaskStatus.NOT_RUN
            
            if task_doc.gateway_node._task_status < task_test.status:
                task_doc.gateway_node._task_status = task_test.status
        
        for task in tasks:
            task_doc = self.get_task_doc(module, task)
            task_doc.gateway_node['classes'].append(task_doc.gateway_node._task_status.css)

        self.process_toctree(doc_name)

        # annotate any top level module sections
        if module and module in self.hierarchy:
            for sect in tree.traverse(section):
                if (
                    isinstance(sect.parent, document) and 
                    any([module in ident.lower() for ident in sect['ids']])
                ):
                    sect['classes'].extend(['module-section', self.hierarchy[module]['status'].css])


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

    def process_toctree(self, app):
        """
        Annoyingly sphinx doc writes each document out as the doctree-resolved hook is
        called. This means we have to process *all* of the toctrees in every document
        when the first document is processed. We do this here. It involves:
            1) Running on all the tests
            2) Walking all of the toctrees and adding the appropriate test status classes
               to the gateway assignment nav bar trees
        """
        if self._app is None:
            self._app = app
            # run all of our tasks
            for _, tasks in task_tests.items():
                for _, task in tasks.items():
                    task.run()
            
            # build the task hierarchy
            self.hierarchy = self.get_gateway_hierarchy()

            # annotate the tree with css status classes
            for _, mod_parts in self.hierarchy.items():
                for node in mod_parts['nodes']:
                    node['classes'].extend(['module', mod_parts['status'].css])
                for _, gtwy_parts in mod_parts['gateways'].items():
                    for node in gtwy_parts['nodes']:
                        node['classes'].extend(['gateway', gtwy_parts['status'].css])
                    for _, task_parts in gtwy_parts['tasks'].items():
                        for node in task_parts['nodes']:
                            node['classes'].extend(['task', task_parts['status'].css])
        return self.hierarchy

    def get_gateway_hierarchy(self):
        """
        Get the gateway task hierarchy from the toctree.
        """
        # module -> gateway -> task
        hierarchy = {}
        module_rgx = re.compile(r'(?P<module>module[\d]+)')
        anchor_rgx = re.compile(r'^#(.*(?P<module>module[\d]+)(?:_[\w]+)?[.-](?:(?P<gateway>gateway[\d]+)(?:_[\w]+)?[.-])?(?:task(?P<task_num>[\d]*)_)?)?(?P<task>[\w-]+)')
        # its really annoying to traverse toc trees, because the link data are not
        # discoverable via parent/child relationships because they are buried in leaf nodes off the parents
        # our strategy here is to try to infer if a given node is a leaf task reference by matching its anchor to known task
        # names for the module it is in
        # this is an insane amount of work to do this... if you're having trouble understanding this code, one of the complexities
        # is that there is not a unified toctree - there is a toctree for each document, and each tree is partial!
        # all this can be a bit brittle and it depends on naming conventions - so stick to the rules!
        for doc_name, toctree in self.app.env.tocs.items():
            match = module_rgx.search(doc_name)
            if match:
                module = match.groupdict()['module']
                hierarchy.setdefault(module, {'gateways': {}, 'nodes': set(), 'status': TaskStatus.NOT_RUN})
                mod_hierarchy = hierarchy[module]
                task_names = set(task_tests.get(module, {}).keys())
                for ref in toctree.traverse(reference):
                    match = anchor_rgx.match(ref.get('anchorname', ''))
                    if match:
                        parts = match.groupdict()

                        # some sanity checks
                        if parts['module'] and parts['module'] != module:
                            continue

                        # spaces and _s may have been permuted to - by the anchor
                        if not (
                            ((task_name := parts['task']) in task_names) or 
                            ((task_name := parts['task'].replace('-', '')) in task_names) or
                            ((task_name := parts['task'].replace('-', '_')) in task_names)
                        ):
                            continue

                        # we have a gateway task reference
                        # walk up the tree and find our list nodes, should be module -> gateway -> task
                        branch = ref
                        while (branch := branch.parent) and not isinstance(branch, list_item):
                            pass
                        task_node = branch
                        assert task_node

                        while (branch := branch.parent) and not isinstance(branch, list_item):
                            pass
                        gateway_node = branch

                        while (branch := branch.parent) and not isinstance(branch, list_item):
                            pass

                        # some partial trees will not have a top level module item
                        if branch:
                            mod_hierarchy['nodes'].add(branch)

                        gateway_name = gateway_node[0][0].astext()
                        mod_hierarchy['gateways'].setdefault(gateway_name, {'nodes': set(), 'tasks': {}, 'status': TaskStatus.NOT_RUN})
                        gtwy_hierarchy = mod_hierarchy['gateways'][gateway_name]
                        if gateway_node:
                            gtwy_hierarchy['nodes'].add(gateway_node)
                        gtwy_hierarchy['tasks'].setdefault(task_name, {'nodes': set(), 'status': TaskStatus.NOT_RUN})
                        gtwy_hierarchy['tasks'][task_name]['nodes'].add(task_node)
                        gtwy_hierarchy['tasks'][task_name]['status'] = task_tests[module][task_name].status

                    elif ref['refuri'] in hierarchy:
                        # we might have a dangling top node, without sub anchors to key off of, in these cases we need to map
                        # to the correct module
                        branch = ref
                        while (branch := branch.parent) and not isinstance(branch, list_item):
                            pass
                        hierarchy[ref['refuri']]['nodes'].add(branch)


        for module, mod_parts in hierarchy.items():
            for _, gtwy_parts in mod_parts['gateways'].items():
                for task_name, task_parts in gtwy_parts['tasks'].items():
                    if gtwy_parts['status'] < task_parts['status']:
                        gtwy_parts['status'] = task_parts['status']

                if mod_parts['status'] < gtwy_parts['status']:
                    mod_parts['status'] = gtwy_parts['status']

        return hierarchy

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
        return self._app or Sphinx(
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
def build(
    detached: bool = typer.Option(
        DETACHED_DEFAULT,
        '--detached',
        help='Generate the docs with no references to the local filesystem.'
    )
):
    """Build the documentation - this will always clean it first."""
    configure_logging()
    clean()
    try:
        import logging
        logging.getLogger('testing').info('[START] docs')
        with doc_context():
            os.system(f'make html SPHINXOPTS="-D detached={int(detached)}"')
    finally:
        logging.getLogger('testing').info('[STOP] docs')
    print(DOC_BLD_DIR / 'html')
    from learn_python.register import do_report
    do_report()

@app.command()
def structure():
    """Spit out a json representation of the course structure."""
    structure = {}
    with ConeOfSilence():
        # todo - ConeOfSilence not entirely effective - still prints some stuff about downloading youtube thumbnails
        for module, tasks in task_map().task_sections.items():
            for task_name, task in tasks.items():
                test = task_map().get_task_test(module, task_name)
                if test:
                    structure.setdefault(module, {})[task_name] = {
                        'number': test.number,
                        'test': test.identifier,
                        'todo': task.todo,
                        'hints': task.hints,
                        'requirements': task.requirements
                    }
    print(json.dumps(structure, indent=4))


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
