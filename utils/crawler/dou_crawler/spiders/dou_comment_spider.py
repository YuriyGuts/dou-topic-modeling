import codecs
import os
import scrapy


class DOUCommentSpider(scrapy.Spider):
    name = "dou-comment-spider"

    start_urls = ["https://dou.ua/lenta/page/{0}/".format(i) for i in range(1, 7)] + \
                 ["https://dou.ua/forums/page/{0}/".format(i) for i in range(1, 11)]

    def parse(self, response):
        for href in response.css("h2 a::attr(href)"):
            topic_url = response.urljoin(href.extract())
            if not topic_url.endswith("comments"):
                yield scrapy.Request(topic_url, callback=self.parse_topic)


    def parse_topic(self, response):
        topic_id = response.url.split("/")[-2]
        result_path = "crawled_data"
        result_prefix = os.path.join(result_path, "comments-") + topic_id

        if not os.path.exists(result_path):
            os.makedirs(result_path)

        with open(result_prefix + ".html", "w") as raw_html_file:
            raw_html_file.write(response.body)

        with codecs.open(result_prefix + ".txt", "w", "utf-8") as comment_file:
            for comment in response.css(".b-comment .text").css("::text").extract():
                comment_file.write(comment)
                comment_file.write("\n" + "-" * 50 + "\n")
