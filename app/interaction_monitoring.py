#!/usr/bin/python3 -u

import queue
import time
import json
from classes.connect_to_extension import Connection
from classes.mutlti_thread_with_queue import ThreadWorkers

con = Connection()

# TODO: We can get number of threads from config file
queue = queue.Queue()
for i in range(5):
    w = ThreadWorkers(queue, con)
    w.setDaemon(True)
    w.start()


while True:
    con.send_message(con.encode_message("start"))  # Send request to Extension for get number of tabs

    tabs_length = con.get_message()

    for i in range(0, int(tabs_length)):  # Get all documents of tabs
        queue.put(con.get_message())

    con.send_message(con.encode_message("stop"))  # Send request to Extension for stop sending document
        
    time.sleep(5)
