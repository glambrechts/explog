import re
import json
import string
import random
import pandas as pd

from pathlib import Path


EXPS_DIRECTORY = Path("exps")
LOGS_DIRECTORY = EXPS_DIRECTORY / "logs"
FORMAT = "[a-zA-Z][a-zA-Z0-9_/]*"


def _identifier(n):
    """
    Sample a random identifier.
    """
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=n))


def exp(*args, **kwargs):
    """
    Initialize an experiment.
    """
    return Experiment(*args, **kwargs)


def init(*args, **kwargs):
    """
    Alias for `exp`.
    """
    return exp(*args, **kwargs)


def log(*args, **logs):
    """
    Check that an experiment already exists.
    """
    if Experiment.current is None:
        raise AttributeError(
            "Initialize an experiment with `explog.exp` before logging.")

    # Log to current run
    Experiment.current.log(*args, **logs)


def exps():
    """
    Retrieve experiments.
    """
    exps = pd.read_json(EXPS_DIRECTORY / "exps.json", lines=True)
    exps = exps.set_index('_id')
    return exps


def runs():
    """
    Alias for `exps`.
    """
    return exps()


def dict_from_kwargs(config=None, *args, **kwargs):
    """
    Returns dictionary from either a single dictionary or kwargs arguments.
    """
    # Check that inputs are keyword arguments or a dictionary
    if len(args) > 1 or (args and kwargs) or (
            config is not None and (args or kwargs)):
        raise ValueError("Usage: log(config) or log(**config).")
    if config is not None:
        args = [config]
    if args and not isinstance(args[0], dict):
        try:
            dictionary = vars(args[0])
        except TypeError:
            raise ValueError("The provided argument should be a dictionary.")
    else:
        dictionary = kwargs

    return dictionary


def logs(*columns, **filters):
    """
    """
    # Retrieve experiments configurations
    exps = pd.read_json(EXPS_DIRECTORY / "exps.json", lines=True)

    # Retrieve experiments logs
    logs = []
    for file in LOGS_DIRECTORY.glob('*.json'):
        log = pd.read_json(file, lines=True)
        log.index.name = '_step'
        log = log.reset_index()
        logs.append(log)
    logs = pd.concat(logs, axis=0)

    # Join configurations and logs
    logs = logs.merge(exps, on='_id')

    # Filter rows
    for key, val in filters.items():
        logs = logs[logs[key] == val]

    # Select columns
    if columns:
        columns = list(columns)
        columns = [c for c in logs.columns if c.startswith('_')] + columns
        logs = logs[columns]

    # Set index
    logs = logs.set_index(['_id', '_step'])

    return logs


class Experiment:
    """
    """
    current = None

    def __init__(self, config=None, *args, id=None, **kwargs):
        # Parse inputs
        config = dict_from_kwargs(config=config, *args, **kwargs)

        # Check configuration keys
        for key in config.keys():
            if not re.fullmatch(FORMAT, key):
                raise ValueError(f"Column '{key}' not in format '{FORMAT}'")

        # Sample random identifier
        self.id = _identifier(8)
        config['_id'] = self.id

        # Store configuration
        with open(EXPS_DIRECTORY / "exps.json", "a") as f:
            f.write(json.dumps(config) + "\n")

        # Store current instance in class
        Experiment.current = self

    def log(self, *args, **kwargs):
        """
        """
        # Parse inputs
        logs = dict_from_kwargs(*args, **kwargs)

        # Check logs keys
        for key in logs.keys():
            if not re.fullmatch(FORMAT, key):
                raise ValueError(f"Column '{key}' not in format '{FORMAT}'")

        logs['_id'] = self.id
        logs_file = (LOGS_DIRECTORY / f"{self.id}.json")
        logs_file.touch()
        with open(logs_file, "a") as f:
            f.write(json.dumps(logs) + "\n")
        logs.pop('_id')

    def logs(self, *columns):
        """
        """
        # Retrieve logged data for this run
        return logs(*columns, _id=self.id)
