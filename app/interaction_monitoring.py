#!/usr/bin/python3 -u

# Note that running python with the `-u` flag is required on Windows,
# in order to ensure that stdin and stdout are opened in binary, rather
# than text, mode.

import json
import sys
import struct


# Read a message from stdin and decode it.
def get_message():
    raw_length = sys.stdin.buffer.read(4)

    if not raw_length:
        sys.exit(0)

    message_length = struct.unpack('=I', raw_length)[0]
    _message = sys.stdin.buffer.read(message_length).decode("utf-8")
    return json.loads(_message)
    # return _message


# Encode a message for transmission, given its content.
def encode_message(message_content):
    encoded_content = json.dumps(message_content).encode("utf-8")
    encoded_length = struct.pack('=I', len(encoded_content))
    #  use struct.pack("10s", bytes), to pack a string of the length of 10 characters

    return {'length': encoded_length, 'content': struct.pack(str(len(encoded_content)) + "s", encoded_content)}


# Send an encoded message to stdout.
def send_message(encoded_message):
    sys.stdout.buffer.write(encoded_message['length'])
    sys.stdout.buffer.write(encoded_message['content'])
    sys.stdout.buffer.flush()


send_message(encode_message(json.dumps({"document": True})))

urls = list()
count = 0

while True:
    data = get_message().split("[[!$asdTTTT12a3sdVV)))*(99999)+")
    if data[0] in urls:
        continue
    urls.append(data[0])

    with open("tmp/logs-{}.html".format(count), "w+") as f:
        # f.write(data[1].strip()[:-1] if data[1][-1] == '"' else data[1].strip())
        f.write(data[1])
    count += 1

