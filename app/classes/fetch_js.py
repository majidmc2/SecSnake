import sys
import scrapy
import os

from scrapy.crawler import CrawlerProcess


class FetchJSFromHTML(scrapy.Spider):
    name = "fetch_js_from_html_file"

    def start_requests(self):
        file = 'file://{}'.format(os.getcwd() + "/" + html_file)
        yield scrapy.Request(url=file, callback=self.parse)

    def parse(self, response):
        javascript_tags = response.css('script::text').getall()

        with open("{}".format(js_file), "w+") as output:
            for js in javascript_tags:
                output.write(js + "\n//--------------------------------------\n")


if __name__ == "__main__":
    html_file = sys.argv[1]
    js_file = sys.argv[2]

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(FetchJSFromHTML)
    process.start()
