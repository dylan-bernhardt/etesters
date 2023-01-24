# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sphinx_rtd_theme
import os
import sys
sys.path.insert(0, os.path.abspath('../../pucs_api/'))


project = 'etesters'
copyright = '2023, Dylan Bernhardt'
author = 'Dylan Bernhardt'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.imgconverter',
    'sphinx_rtd_theme',
    "autodocsumm",
    "autoclass",
    "sphinx_rtd_size",
]


autodoc_default_options = {
    "autosummary": True,
    'member-order': 'groupwise',  # 'bysource', 'alphabetical', 'groupwise'
    'special-members': '__init__',
}
sphinx_rtd_size_width = "90%"

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
