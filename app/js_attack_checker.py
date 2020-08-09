#!/usr/bin/python3 -u

import json
from classes.connect_to_extension import Connection


con = Connection()
# con.send_message(con.encode_message(json.dumps({"check": True})))

urls = list()

while True:
    data = con.get_message().split("[[!$AsdTTTT12a3sdVV)))*(888888)+")
    html_file = data[0]
    url = data[1]

    if url in urls:
        continue
    urls.append(url)

    # get filename of html and then get js of it and save after that check with 'semgrep'

    with open("logs.txt", "a+") as f:
        f.write(html_file + ".html\n")
