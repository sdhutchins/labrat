# -*- coding: utf-8 -*-
import json
from pathlib import Path


def get_labrat_dir() -> Path:
    """
    Get the .labrat directory path in the user's home directory.

    Creates the directory if it doesn't exist. This directory is used for
    storing logs, archives, and other labrat-related files.

    Returns:
        Path: Path to the .labrat directory in the user's home directory.

    Example:
        >>> labrat_dir = get_labrat_dir()
        >>> log_file = labrat_dir / "archive.log"
    """
    labrat_dir = Path.home() / ".labrat"
    # Create directory if it doesn't exist (cross-platform compatible)
    labrat_dir.mkdir(exist_ok=True)
    return labrat_dir


def import_json(json_file):
    """Import json and convert it to a dictionary."""
    with open(json_file) as jsonfile:
        # `json.loads` parses a string in json format
        file_dict = json.load(jsonfile)
        return file_dict
