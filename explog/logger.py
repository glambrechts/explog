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
    # Sample a random identifier
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=n))


def init(config):
    # Initialize an experiment
    return Experiment(config)


def exps(*columns):
    # Retrieve experiments
    exps = pd.read_json(EXPS_DIRECTORY / "exps.json", lines=True)
    exps = exps.set_index('_id')
    return exps


def logs(*columns, **filters):
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
    def __init__(self, config):
        # Check that configuration is a dictionary
        if not isinstance(config, dict):
            config = vars(config)

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

    def log(self, *args, **logs):
        # Check that inputs are keyword arguments or a dictionary
        if len(args) > 1 or (args and logs):
            raise ValueError("Usage: log(dictionary) or log(**dictionary).")
        if args and not isinstance(args[0], dict):
            raise ValueError("The provided argument should be a dictionary.")

        # Retrieve dictionary
        if args:
            logs = args[0]

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

    def get(self, *columns):
        # Retrieve logged data for this run
        return logs(*columns, _id=self.id)
