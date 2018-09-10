import scrapy
from utils import parse_art_page, get_page_categories


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        # 'http://pstrial-2018-05-21.toscrape.com/browse/insunsh',
        # 'http://pstrial-2018-05-21.toscrape.com/browse/summertime',
        'http://pstrial-2018-05-21.toscrape.com/browse/summertime/rossignolnachtigall'
    ]

    def parse_art_pages(self, response):
        art_links = response.css('a[href*=item]::attr("href")').extract()

        if len(art_links) == 0:
            return None

        for art_link in art_links:
            extra_info = {'url': art_link, 'path': 'test'}
            callback = lambda response: parse_art_page(response, extra_info)
            yield response.follow(art_link, callback)

        next_page = response.css('a:contains(Next)::attr("href")').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse_art_pages)

    def parse(self, response):
        categories = get_page_categories(response)

        if len(categories) == 0:
            for art_request in self.parse_art_pages(response):
                yield art_request
        else:
            for key, category in categories.items():
                link = category['link']
                sublinks = category['sublinks']
                if len(sublinks) > 0:
                    for sublink in sublinks:
                        yield response.follow(sublink, self.parse_art_pages)
                else:
                    yield response.follow(link, self.parse_art_pages)
