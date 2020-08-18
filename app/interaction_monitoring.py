#!/usr/bin/python3 -u

import queue
import time
import sys
import json

from classes.connect_to_extension import Connection
from classes.mutlti_thread_with_queue import ThreadWorkers


con = Connection()
thread = 5       # Thread by Default
interval = 10    # Second by Default


with open("../attack_pattern.json", "r") as conf_file:
    configure = json.load(conf_file)
    if "interaction_monitoring" not in configure:
        con.send_message(con.encode_message(json.dumps({"status": "no-config"})))
        sys.exit()  # Exit from this code because InteractionMonitoring isn't configured
    if "configuration" in configure:
        if "interval" in configure["configuration"]:
            if configure["configuration"]["interval"] > 10 or configure["configuration"]["interval"] == -1:
                interval = configure["configuration"]["interval"]
        if "thread" in configure["configuration"]:
            if configure["configuration"]["thread"] > 5:
                thread = configure["configuration"]["thread"]

queue = queue.Queue()
for i in range(thread):
    w = ThreadWorkers(queue, con, configure)
    w.setDaemon(True)
    w.start()

while True:
    # Send request to Extension for get number of tabs
    con.send_message(con.encode_message(json.dumps({"status": "start"})))

    tabs_length = con.get_message()

    # Get all documents of tabs
    for i in range(0, int(tabs_length)):
        queue.put(con.get_message())

    # Send request to Extension for stop sending document
    con.send_message(con.encode_message(json.dumps({"status": "stop"})))

    if interval == -1:
        queue.join()
        sys.exit()  # Just for one time

    time.sleep(interval)
