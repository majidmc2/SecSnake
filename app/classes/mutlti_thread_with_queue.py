import threading
import string
import random
import os
import json


class ThreadWorkers(threading.Thread):
    def __init__(self, queue, connection, attack_pattern):
        super().__init__()

        self.queue = queue
        self.connection = connection
        self.attack_pattern = attack_pattern
        self.html_file = None
        self.js_file = None
        self.url = None

    def __create_random_file_name(self, _format):
        file_name = "".join(random.choice(
            string.ascii_uppercase + string.ascii_lowercase + string.digits
        ) for _ in range(20)) + _format
        return file_name

    def __file_deleter(self, _file):
        os.system("rm -rf {}".format(_file))

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

    def __semgrep(self, _pattern_file):
        with open("{}".format(_pattern_file)) as pf:
            for pattern in pf.readlines():
                cmd = """semgrep --lang javascript --json --pattern "{pattern}" tmp/javascript/{file}""".format(
                                                                                pattern=pattern[:-1], file=self.js_file)
                with os.popen(cmd) as semgrep:
                    result = json.loads(semgrep.read())
                    if result["results"]:
                        for r in result["results"]:
                            self.connection.send_message(self.connection.encode_message(json.dumps(
                                {
                                    "status": "find-attack",
                                    "title": "Interaction Monitoring",
                                    "message": "Find attack pattern in JavaScript codes",
                                    "contextMessage": "Pattern: {pattern}\nURL: {url}\nline:{line}\nextract:{extract}"
                                    .format(
                                        pattern=pattern,
                                        url=self.url,
                                        line=r["start"]["line"],
                                        extract=r["extra"]["message"]
                                    )
                                }
                            )))

        self.__file_deleter("tmp/javascript/{file}".format(file=self.js_file))

    def __check_html_patterns(self):

        def run_checker(pattern, tag, attribute, witch):
            output_file = self.__create_random_file_name(".json")
            cmd = "python3 classes/check_html_pattern.py tmp/html/{input} {patterns} {tag} {attribute}" \
                  " tmp/find_html_pattern/{out} {witch}"\
                                                    .format(
                                                        input=self.html_file,
                                                        patterns=pattern,
                                                        tag=tag,
                                                        attribute="NO-ATT" if attribute == "" else attribute,
                                                        out=output_file,
                                                        witch=witch
                                                    )
            os.system(cmd)

            with open("tmp/find_html_pattern/{out}".format(out=output_file), "r+") as ch:
                result = json.loads(ch.read())
                if result["results"]:
                    for r in result["results"]:
                        if witch == "data":
                            self.connection.send_message(self.connection.encode_message(json.dumps(
                                {
                                    "status": "find-attack",
                                    "title": "Interaction Monitoring",
                                    "message": "Find attack pattern in HTML",
                                    "contextMessage": "Pattern: {pattern}\nURL: {url}\nTag: {tag}".format(
                                                                                                    pattern=r[1],
                                                                                                    url=self.url,
                                                                                                    tag=r[0]
                                                                                                )
                                }
                            )))

                        elif witch == "regexp":
                            self.connection.send_message(self.connection.encode_message(json.dumps(
                                {
                                    "status": "find-attack",
                                    "title": "Interaction Monitoring",
                                    "message": "Find attack pattern in HTML",
                                    "contextMessage": "URL: {url}\nExtract: {extract}".format(
                                        url=self.url,
                                        extract=', '.join(r)
                                    )
                                }
                            )))

            self.__file_deleter("tmp/find_html_pattern/{out}".format(out=output_file))

        for e in self.attack_pattern["interaction_monitoring"]["element"]:
            if "data" in e["check"]:
                run_checker(e["check"]["data"], e["tag"], e["attribute"], "data")

            if "regexp" in e["check"]:
                run_checker(e["check"]["regexp"], e["tag"], e["attribute"], "regexp")

    def __check_css_patterns(self):
        for css in self.attack_pattern["interaction_monitoring"]["css"]:
            output_file = self.__create_random_file_name(".json")
            css_value = ""
            condition = ""
            if "if_equal" in css["check"]:
                condition = "if_equal"
                css_value = css["check"]["if_equal"]
            elif "if_lees_than" in css["check"]:
                condition = "if_lees_than"
                css_value = css["check"]["if_lees_than"]
            elif "if_more_than" in css["check"]:
                condition = "if_more_than"
                css_value = css["check"]["if_more_than"]

            cmd = "python3 classes/check_css_pattern.py tmp/html/{input} {tag} {css_property} {css_value} {condition} " \
                  "tmp/find_html_pattern/{out}".format(
                                                    input=self.html_file,
                                                    tag=css["tag"],
                                                    css_property=css["property"],
                                                    css_value=css_value,
                                                    condition=condition,
                                                    out=output_file,
                                                )

            os.system(cmd)

            with open("tmp/find_html_pattern/{out}".format(out=output_file), "r+") as ch:
                result = json.loads(ch.read())
                if result["results"]:
                    for r in result["results"]:
                        with open("logs.txt", "a+") as l: l.write("{}\n".format(r))
                        self.connection.send_message(self.connection.encode_message(json.dumps(
                            {
                                "status": "find-attack",
                                "title": "Interaction Monitoring",
                                "message": "Find attack pattern in HTML",
                                "contextMessage": "URL: {url}\nCondition:{condition}\nProperty: {css_property}\n"
                                                                                    .format(
                                                                                            url=self.url,
                                                                                            condition=condition,
                                                                                            css_property=r[condition],
                                                                                    )
                            }
                        )))
            self.__file_deleter("tmp/find_html_pattern/{out}".format(out=output_file))

    def __task_done(self):
        self.queue.task_done()

    def run(self):
        while True:
            self.__save_html_file()

            # Check JavaScript patterns
            if "javascript" in self.attack_pattern["interaction_monitoring"]:
                self.__extract_js_code()
                js_pattern_file = self.attack_pattern["interaction_monitoring"]["javascript"]["pattern"]
                self.__semgrep(js_pattern_file)

            # Check HTML patterns
            if "element" in self.attack_pattern["interaction_monitoring"]:
                if self.attack_pattern["interaction_monitoring"]["element"]:
                    self.__check_html_patterns()
                else:
                    pass
                    # TODO: Send message error to Extension

            # Check CSS values
            if "css" in self.attack_pattern["interaction_monitoring"]:
                if self.attack_pattern["interaction_monitoring"]["css"]:
                    self.__check_css_patterns()
                else:
                    pass
                    # TODO: Send message error to Extension

            self.__task_done()
