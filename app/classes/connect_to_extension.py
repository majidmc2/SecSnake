import json
import sys
import struct


class Connection:

    def get_message(self):
        '''Read a message from stdin and decode it.'''
        
        raw_length = sys.stdin.buffer.read(4)

        if not raw_length:
            sys.exit(0)

        message_length = struct.unpack('=I', raw_length)[0]
        _message = sys.stdin.buffer.read(message_length).decode("utf-8")
        return json.loads(_message)
        # return _message

    def encode_message(self, message_content):
        '''Encode a message for transmission, given its content.'''
       
        encoded_content = json.dumps(message_content).encode("utf-8")
        encoded_length = struct.pack('=I', len(encoded_content))
        #  use struct.pack("10s", bytes), to pack a string of the length of 10 characters

        return {'length': encoded_length, 'content': struct.pack(str(len(encoded_content)) + "s", encoded_content)}

    def send_message(self, encoded_message):
        '''Send an encoded message to stdout.'''
        
        sys.stdout.buffer.write(encoded_message['length'])
        sys.stdout.buffer.write(encoded_message['content'])
        sys.stdout.buffer.flush()
