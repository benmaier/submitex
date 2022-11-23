# -*- coding: utf-8 -*-
"""
Initializes this package with metadata.
"""

from .metadata import (
        __version__,
        __author__,
        __copyright__,
        __credits__,
        __license__,
        __maintainer__,
        __email__,
        __status__,
    )

from .resolveinputs import convert as resolve_inputs
from .resolvepipes import convert as resolve_input_commands
from .collectfloats import convert as collect_floats
from .collectfloats import extract_floats
from .replacebib import convert as replace_bib
from .replacefigs import convert_and_get_figure_paths as rename_figures_and_get_paths
