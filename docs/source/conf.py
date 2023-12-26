from sphinx.util.docutils import SphinxDirective
from docutils import nodes

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'learn-python'
copyright = '2023, Brian Kohan'
author = 'Brian Kohan'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
html_favicon = 'favicon.ico'
#html_logo = 'logo.svg'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx_rtd_theme',
    'sphinxcontrib.youtube',
    'sphinxcontrib.jquery',
    'learn_python.doc',
    'sphinx_click',
    'sphinxcontrib.typer',
]

master_doc = 'index'

html_theme = "sphinx_rtd_theme"

html_css_files = [
    'learn_python.css',
    'termynal.css',
]
html_js_files = [
    'learn_python.js',
    'termynal.js',
]

html_static_path = ['_static']

todo_include_todos = True
source_encoding = 'utf-8-sig'
