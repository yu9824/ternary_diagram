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
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))


# -- Project information -----------------------------------------------------

project = 'ternary-diagram'
copyright = '2021, yu9824'
author = 'yu9824'

# The full version, including alpha/beta/rc tags
from ternary_diagram import __version__
release = __version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
# extensions = [
# ]
extensions = [
    'sphinx.ext.autodoc',       # docstringからドキュメントを作成してくれる．
    'sphinx.ext.napoleon',      # google式・numpy式docstringを整形してくれる．
    'sphinx.ext.githubpages',   # github-pages用のファイルを生成してくれる．
    'recommonmark',             # markdownで書けるようにする．
    'sphinx_markdown_tables',   # markdownの表を書けるようにする．
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['setup']

# markdown
source_suffix = ['.rst', '.md']
source_parsers = {
   '.md': 'recommonmark.parser.CommonMarkParser',
}

from shutil import copyfile
fname_readme = 'README.md'
path_readme = os.path.join(os.path.abspath('../..'), 'README.md')
if os.path.isfile(path_readme):
    copyfile(path_readme, fname_readme)
else:
    print(path_readme)


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'alabaster'
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']