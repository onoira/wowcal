#!/usr/bin/env python3

import json
import os.path as path
import sys

import jsonschema
import jsonschema.exceptions as jsonexceptions
import yaml


if len(sys.argv) < 2:
    sys.exit("Usage: validate /path/to/file.yml")

filepath = path.abspath(sys.argv[1])
if not path.exists(filepath):
    print(f"No such file '{filepath}'")

schema:dict
with open('schema.json', 'r') as fp:
    schema = json.load(fp)

datum:dict
with open(filepath, 'r') as fp:
    datum = yaml.load(fp, Loader=yaml.FullLoader)

try:
    jsonschema.validate(datum, schema)
except jsonexceptions.ValidationError as e:
    print("Invalid schema:", e)
except jsonexceptions.JSONDecodeError:
    print("Invalid JSON:", e)
