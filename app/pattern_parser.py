#!/usr/bin/python3 -u


import json
import jsonschema
from jsonschema import validate
from classes.connect_to_extension import Connection
from classes.attack_pattern_schema import AttackPatternSchema


def validate_json(_json_data):
    try:
        validate(instance=_json_data, schema=AttackPatternSchema)
    except jsonschema.exceptions.ValidationError:
        return False
    return True


con = Connection()

try:
    conf_file = open("../attack_pattern.json", "r")
except FileNotFoundError:
    con.send_message(con.encode_message(json.dumps({"parsed": False, "error": "No such file 'attack_pattern.json'"})))
else:
    try:
        json_data = json.load(conf_file)
    except ValueError or json.decoder.JSONDecodeError:
        con.send_message(con.encode_message(json.dumps(
            {"parsed": False, "error": "Given attack pattern file is invalid to load"})))
    else:
        is_valid = validate_json(json_data)
        if is_valid:
            con.send_message(con.encode_message(json.dumps({"parsed": True})))
        else:
            con.send_message(con.encode_message(json.dumps(
                {"parsed": False, "error": "Given attack pattern file has invalid syntax"})))
