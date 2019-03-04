# -*- coding: utf-8 -*-
import json


def import_json(json_file):
    """Import json and convert it to a dictionary."""
    with open(json_file) as jsonfile:
        # `json.loads` parses a string in json format
        file_dict = json.load(jsonfile)
        return file_dict
