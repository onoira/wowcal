from __future__ import annotations

from wowcal.__version__ import __author__
from wowcal.__version__ import __author_email__
from wowcal.__version__ import __license__
from wowcal.__version__ import __version__
from wowcal.__version__ import VERSION as __VERSION

from wowcal import models


def get_version() -> tuple[int]:
    return __VERSION
