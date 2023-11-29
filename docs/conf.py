# SPDX-FileCopyrightText: 2023 GSI Helmholtzzentrum fuer Schwerionenforschung GmbH, Darmstadt, Germany
#
# SPDX-License-Identifier: LGPL-3.0-only

import os
from sphinx.ext.apidoc import main as sphinx_apidoc
import sys


_ROOT = os.path.abspath("../src")
sys.path.insert(0, _ROOT)

github_username = "GSI-HPC"
github_repository = "py-ina238"
author = "Dennis Klein"
project = "ina238"
copyright = "2023 GSI Helmholtz Zentrum fuer Schwerionenforschung GmbH"
language = "en"
extensions = [
    "sphinx_toolbox",
    "sphinx_toolbox.more_autodoc",
    "sphinx_toolbox.more_autosummary",
    "sphinx_toolbox.tweaks.param_dash",
    "sphinx_toolbox.tweaks.latex_layout",
    "sphinx_toolbox.tweaks.latex_toc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinxcontrib.extras_require",
    "sphinx.ext.todo",
    "sphinxemoji.sphinxemoji",
    "notfound.extension",
    "sphinx_copybutton",
    "sphinxcontrib.default_values",
    "sphinx_debuginfo",
    "sphinx_licenseinfo",
    "html_section",
    "sphinx.ext.autodoc",
    "sphinx.ext.githubpages",
    "sphinx_multiversion",
    "sphinx.ext.extlinks",
]
sphinxemoji_style = "twemoji"
gitstamp_fmt = "%d %b %Y"
templates_path = [
    "_templates",
]
source_suffix = ".rst"
master_doc = "index"
suppress_warnings = [
    "image.nonlocal_uri",
]
pygments_style = "default"
html_theme = "sphinx_rtd_theme"
html_show_sourcelink = True
toctree_plus_types = [
    "class",
    "confval",
    "data",
    "directive",
    "enum",
    "exception",
    "flag",
    "function",
    "namedtuple",
    "protocol",
    "role",
    "typeddict",
]
add_module_names = False
hide_none_rtype = True
all_typevars = True
overloads_location = "bottom"
html_codeblock_linenos_style = "table"
intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}
smv_tag_whitelist = r"^v[1-9]\d*\.\d+\.\d+$"
smv_branch_whitelist = r"^main$"
smv_remote_whitelist = None
smv_released_pattern = r"^refs/tags/.*$"
smv_outputdir_format = "{ref.name}"
html_theme_options = {
    "display_version": False,
    "prev_next_buttons_location": "both",
}
display_github = True
github_url = "https://github.com/GSI-HPC/py-ina238"
extlinks = {
    "datasheet": (
        "https://www.ti.com/document-viewer/INA238/datasheet/%s",
        "Datasheet[%s]",
    )
}
