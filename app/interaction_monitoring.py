#!/usr/bin/python3 -u

import json
from classes.connect_to_extension import Connection


con = Connection()
con.send_message(con.encode_message(json.dumps({"document": True})))

urls = list()
while True:
    data_first = con.get_message().split("[[!$asdTTTT12a3sdVV)))*(99999)+")
    data_second = data_first[0].split("[[!$AsdTTTT12a3sdVV)))*(888888)+")

    code = data_first[1]
    url = data_second[1]
    file_name = data_second[0]

    if url in urls:
        continue
    urls.append(url)

    with open("tmp/html/{}.html".format(file_name), "w+") as f:
        f.write(code)
