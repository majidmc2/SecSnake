import sys
import scrapy
import os
import json

from scrapy.crawler import CrawlerProcess


class FetchJSFromHTML(scrapy.Spider):
    name = "fetch_js_from_html_file"

    def start_requests(self):
        file = 'file://{}'.format(os.getcwd() + "/" + html_file)
        yield scrapy.Request(url=file, callback=self.parse)

    def parse(self, response):
        if attribute:
            tags = response.css('{tag}::attr({att})'.format(tag=tag, att=attribute)).getall()
        else:
            tags = response.css('{tag}'.format(tag=tag)).getall()

        result = {"results": []}

        for t in tags:
            with open("{}".format(pattern_file), "r") as pt:
                for p in pt.readlines():
                    if t.strip() == p.strip():
                        result["results"].append([t, p])

        with open("tmp/find_html_pattern/{output}".format(output=output.replace("html", "json")), "w+") as output_file:
            output_file.write(json.dumps(result))


if __name__ == "__main__":
    html_file = sys.argv[1]
    pattern_file = sys.argv[2]
    tag = sys.argv[3]
    attribute = sys.argv[4]
    output = sys.argv[5]

    if attribute == "NO-ATT":
        attribute = None

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(FetchJSFromHTML)
    process.start()
