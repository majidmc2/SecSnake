import threading
import string
import random
import os


class ThreadWorkers(threading.Thread):
    def __init__(self, queue, connection):
        super().__init__()

        self.queue = queue
        self.connection = connection
        self.attack_pattern = None
        self.html_file = None
        self.js_file = None
        self.url = None

    def __create_random_file_name(self, _format):
        file_name =  "".join(random.choice(
            string.ascii_uppercase + string.ascii_lowercase + string.digits
        ) for _ in range(20)) + _format
        return file_name

    def __save_html_file(self):
        data = self.queue.get().split("--//*****Split*****//--")
        self.url = data[0]
        code = data[1]

        self.html_file = self.__create_random_file_name(".html")

        with open("tmp/html/{}".format(self.html_file), "w+") as html_file:
            html_file.write(code)

    def __extract_js_code(self):
        """Because 'Scrapy' runs in main thread we run this file"""
        self.js_file = self.__create_random_file_name(".js")
        os.system("python3 classes/fetch_js.py tmp/html/{input} tmp/javascript/{output}"
                  .format(input=self.html_file, output=self.js_file))

    def __task_done(self):
        self.queue.task_done()

    def run(self):
        while True:
            self.__save_html_file()
            self.__extract_js_code()
            self.__task_done()
