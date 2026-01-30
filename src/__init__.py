import sys
from pathlib import Path

_src_root = Path(__file__).parent
_progect_root = _src_root.parent

if str(_progect_root) not in sys.path:
    sys.path.insert(0,str(_progect_root))

from . import app
from . import core
from . import modules

__all__= ['app','core','modules']