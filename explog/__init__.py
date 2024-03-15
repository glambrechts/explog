from .logger import EXPS_DIRECTORY, LOGS_DIRECTORY
from .logger import init, exps, logs


EXPS_DIRECTORY.mkdir(parents=True, exist_ok=True)
LOGS_DIRECTORY.mkdir(parents=True, exist_ok=True)
