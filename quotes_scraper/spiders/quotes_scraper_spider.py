import scrapy
import logging

class QuotesSpider(scrapy.Spider):
    name = 'quotes_scraper'
    root_url = '' # url of site removed for privacy reasons
    start_urls = [''] # url of site removed for privacy reasons
    quotes_added = []

    def parse(self, response):
        first_line = response.xpath('//*[@id="qbc1"]/div')
        dict_quote = {}

        for item in first_line:
            quote_text = item.xpath("./a[1]/div[1]/text()").get()
            quote_author = item.xpath("./a[2]/text()").get()


            if (quote_text is not None or "") or (quote_author is not None or ""):
                quote_text = str(quote_text).replace("\n", "")
                if quote_text not in self.quotes_added:
                    self.quotes_added.append(quote_text)
                    dict_quote = {
                        'quote_text': quote_text,
                        'quote_author': quote_author
                    }
                    yield dict_quote

        pagination_list = response.xpath("/html/body/main/div[3]/div[1]/ul[1]/li")

        for item in pagination_list:
            item_text = item.get()
            if "Next" in item_text:
                next_href = item.xpath('./a[1]').attrib['href']
                next_page_url = self.root_url + next_href
                yield response.follow(next_page_url, callback=self.parse)
