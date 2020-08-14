import sys
import scrapy
import os
import json
import cssutils

from scrapy.crawler import CrawlerProcess


class FetchJSFromHTML(scrapy.Spider):
    name = "check_css_patterns_on_html_file"

    def start_requests(self):
        file = 'file://{}'.format(os.getcwd() + "/" + html_file)
        yield scrapy.Request(url=file, callback=self.parse)

    def parse(self, response):

        result = {"results": []}

        tags = response.css('{tag}::attr(style)'.format(tag=tag)).getall()
        for t in tags:
            arsed_css = dict(cssutils.parseStyle(t))
            if css_property in arsed_css:
                property_value = arsed_css[css_property]

                if condition == "if_equal":
                    _css_value = css_value
                    if str(css_value).isdigit() and str(property_value).isdigit():
                        property_value = float(property_value)
                        _css_value = float(css_value)
                    if property_value == _css_value:
                        result["results"].append({condition: "{}:{}".format(css_property, property_value)})

                elif condition == "if_lees_than":
                    if float(property_value) < float(css_value):
                        result["results"].append({condition: "{}:{}".format(css_property, property_value)})

                elif condition == "if_more_than":
                    if float(property_value) > float(css_value):
                        result["results"].append({condition: "{}:{}".format(css_property, property_value)})

        with open("{output}".format(output=output), "w+") as output_file:
            output_file.write(json.dumps(result))


if __name__ == "__main__":
    html_file = sys.argv[1]
    tag = sys.argv[2]
    css_property = sys.argv[3]
    css_value = sys.argv[4]
    condition = sys.argv[5]
    output = sys.argv[6]

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(FetchJSFromHTML)
    process.start()
