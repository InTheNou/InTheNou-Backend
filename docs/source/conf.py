# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import sphinx_rtd_theme
import os
import sys
sys.path.insert(0, os.path.abspath('../../flask'))


# -- Project information -----------------------------------------------------

project = 'InTheNou Backend'
copyright = '2020, Diego J. Amador Bonilla & Brian Rodriguez Badillo'
author = 'Diego J. Amador Bonilla & Brian Rodriguez Badillo'

# The full version, including alpha/beta/rc tags
release = '0.0.1'

master_doc = 'index'
# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.coverage',
              'sphinx.ext.napoleon',
              'sphinxcontrib.httpdomain',
              'sphinxcontrib.autohttp.flask',
              'sphinxcontrib.autohttp.flaskqref',
              'sphinx.ext.todo',
              'sphinx.ext.githubpages',
              "sphinx_rtd_theme"
]
napoleon_google_docstring = False
napoleon_use_param = False
napoleon_use_ivar = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
# pygments_style = 'sphinx'

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.

html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_css_files = ['nowidth.css']

# autodoc_mock_imports = []

latex_elements = {
    'printindex': '\\footnotesize\\raggedright\\printindex',
'preamble': r'\let\oldmultirow\multirow\def\multirow#1#2{\oldmultirow{#1}{=}}',
}
