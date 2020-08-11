#!/usr/bin/python3 -u

import json
from classes.connect_to_extension import Connection


con = Connection()

try:
    with open("../configuration.json", "r") as conf_file:
        pass

    con.send_message(con.encode_message(json.dumps({"parsed": True})))

except:
    con.send_message(con.encode_message(json.dumps({"parsed": False, "error": "No such file 'ciguration.json'"})))
