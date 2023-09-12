from docutils.parsers.rst import Parser
from docutils.utils import new_document
from docutils.nodes import Admonition
from dataclasses import dataclass, field
from typing import Optional
from types import ModuleType
from functools import cached_property
from docutils.parsers.rst import Parser
from docutils.utils import new_document
from sphinx.environment import BuildEnvironment
from sphinx.config import Config
from sphinx.application import Sphinx
from docutils import frontend
from pathlib import Path
import re


@dataclass
class Assignment:
    """Data structure for storing assignment information"""



class Tutor:
    """
    A base class for Tutor implementations. This class is responsible for the common tutoring tasks
    like extracting structured information from the gateway assignment docstring. Implementations of
    tutors for specific LLMs or AI platforms should inherit from this class.
    """

    assignments = {}

    def __init__(self):
        pass

    def start_session(self, assignment):
        pass


    

    def parse_assignments(self):
        module_rgx = re.compile('(module\d+)')
        for doc_name in self.app.env.found_docs:
            if 'gateway' in doc_name:
                module = module_rgx.search(doc_name).groups(1)
                import ipdb
                ipdb.set_trace()
                for node in self.app.env.get_doctree(doc_name):
                    # todo build a mapping of section nodes to their corresponding test and task
                    pass


