github_username = 'GSI-HPC'
github_repository = 'py-ina238'
author = 'Dennis Klein'
project = 'py-in238'
copyright = '2023 GSI Helmholtz Zentrum fuer Schwerionenforschung GmbH'
language = 'en'
package_root = 'ti'
extensions = [
    'sphinx_toolbox',
    'sphinx_toolbox.more_autodoc',
    'sphinx_toolbox.more_autosummary',
    #  'sphinx_toolbox.documentation_summary',
    'sphinx_toolbox.tweaks.param_dash',
    'sphinx_toolbox.tweaks.latex_layout',
    'sphinx_toolbox.tweaks.latex_toc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
    'sphinxcontrib.extras_require',
    'sphinx.ext.todo',
    'sphinxemoji.sphinxemoji',
    'notfound.extension',
    'sphinx_copybutton',
    'sphinxcontrib.default_values',
    #  'sphinxcontrib.toctree_plus',
    'sphinx_debuginfo',
    'sphinx_licenseinfo',
    'seed_intersphinx_mapping',
    'html_section',
    #  'sphinx_toolbox_experimental.autosummary_widths',
    #  'sphinx_toolbox_experimental.succinct_seealso',
    #  'sphinx_toolbox_experimental.needspace',
    #  'sphinx_toolbox_experimental.missing_xref',
    #  'sphinx_toolbox_experimental.changelog',
    #  'sphinx_toolbox_experimental.peps',
]
sphinxemoji_style = 'twemoji'
gitstamp_fmt = '%d %b %Y'
templates_path = [ '_templates',]
#  html_static_path = [ '_static',]
source_suffix = '.rst'
master_doc = 'index'
suppress_warnings = [ 'image.nonlocal_uri',]
pygments_style = 'default'
html_theme = 'classic'
html_show_sourcelink = True
toctree_plus_types = [
    'class',
    'confval',
    'data',
    'directive',
    'enum',
    'exception',
    'flag',
    'function',
    'namedtuple',
    'protocol',
    'role',
    'typeddict',
]
add_module_names = False
hide_none_rtype = True
all_typevars = True
overloads_location = 'bottom'
html_codeblock_linenos_style = 'table'
autodoc_exclude_members = [
    '__dict__',
    '__class__',
    '__dir__',
    '__weakref__',
    '__module__',
    '__annotations__',
    '__orig_bases__',
    '__parameters__',
    '__subclasshook__',
    '__init_subclass__',
    '__attrs_attrs__',
    '__init__',
    '__new__',
    '__getnewargs__',
    '__abstractmethods__',
    '__hash__',
]
intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}
