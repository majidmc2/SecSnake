import threading
import time
import string
import random


class ThreadWorkers(threading.Thread):
    def __init__(self, queue, connection):
        super().__init__()
        self.queue = queue
        self.connection = connection
        self.url = None

    def __save_html_file(self):
        data = self.queue.get().split("--//*****Split*****//--")
        self.url = data[0]
        code = data[1]

        file_name = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
                            for _ in range(20))
        with open("tmp/html/{}.html".format(file_name), "w+") as html_file:
            html_file.write(code)

    def __queue_task_done(self):
        self.queue.task_done()

    def run(self):
        while True:
            self.__save_html_file()
            # time.sleep(10)
            self.__queue_task_done()
