#!/usr/bin/python3 -u

import json
import sys

from classes.connect_to_extension import Connection


con = Connection()


with open("../attack_pattern.json", "r") as conf_file:
    configure = json.load(conf_file)

    if "on_before_request" not in configure:
        con.send_message(con.encode_message(json.dumps({"status": "no-config"})))
        sys.exit()  # Exit from this code because InteractionMonitoring isn't configured

    else:
        con.send_message(con.encode_message(json.dumps({"status": "start", "data": configure["on_before_request"]})))
