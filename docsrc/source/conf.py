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
import datetime
import numpy
sys.path.insert(0, os.path.abspath('../..'))
from zap_me_not import __about__ as metadata
# sys.path.insert(0, os.path.join(os.path.abspath('../..'),'zap_me_not'))


# -- Project information -----------------------------------------------------
# Handled by metadata import
#project = 'ZapMeNot'
#copyright = '2020, Alan Ford'
author = metadata.__author__

# The full version, including alpha/beta/rc tags
#release = '0.0.1'
# The short X.Y version.
version = metadata.__version__
# The full version, including alpha/beta/rc tags.
release = metadata.__version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.napoleon',
	'sphinx.ext.todo',
	'sphinx.ext.autodoc',
	'sphinx.ext.viewcode',
	'sphinx.ext.doctest',
	'sphinx.ext.mathjax',
	'sphinx.ext.intersphinx',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = metadata.__package_name__.replace('-', '').capitalize()
copyright = u'%s,  %s' % (
    datetime.date.today().year,
    metadata.__author__,
)

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
# The paper size ('letterpaper' or 'a4paper').
'papersize': 'letterpaper',

# The font size ('10pt', '11pt' or '12pt').
'pointsize': '10pt',

# Additional stuff for the LaTeX preamble.
'preamble': '',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [(
    'index',
    '%s.tex' % metadata.__package_name__,
    u'%s Documentation' % metadata.__package_name__.replace('-', ' ').capitalize(),
   metadata.__author__,
   'manual',
)]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# If true, show page references after internal links.
#latex_show_pagerefs = False

# If true, show URL addresses after external links.
#latex_show_urls = False

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_domain_indices = True


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'wolph'
# html_theme = 'alabaster'
html_theme = "sphinx_rtd_theme"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
# html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
# html_theme_path = ['_theme']

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
# html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
# html_short_title = 'ZapMeNot docs'

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
# html_favicon = 'favicon.ico'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_last_updated_fmt = '%b %d, %Y'

# Output file base name for HTML help builder.
# htmlhelp_basename = 'zapmenotdoc'

# support for numpy and google style docstrings
napoleon_use_ivar = True

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# This is required for the alabaster theme
# refs: http://alabaster.readthedocs.io/en/latest/installation.html#sidebars
html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',  # needs 'show_related': True theme option to display
        'searchbox.html',
        'donate.html',
    ]
}

# Example configuration for intersphinx: refer to the Python standard library.
#  Intersphinx permits links to other projects' documentation
# intersphinx_mapping = {
#     'python': ('https://docs.python.org/3/', None),
#     'pythonutils': ('https://python-utils.readthedocs.io/en/latest/', None),
#     'numpy': ('https://numpy.org/doc/stable/', None),
#     'scipy': ('https://docs.scipy.org/doc/scipy/reference/', None)
# }
