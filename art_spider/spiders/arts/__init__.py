# -*- coding: utf-8 -*-
import scrapy
from art_spider.spiders.arts.utils import parse_art_page, get_page_categories, get_tree_path
from art_spider.spiders.arts.config import BASE_URL, START_CATEGORIES


class ArtsSpider(scrapy.Spider):
    name = "arts"
    start_urls = [
        BASE_URL + '/browse/'
    ]

    def parse_art_pages(self, response):
        headers = response.request.headers
        art_urls = response.css('a[href*=item]::attr("href")').extract()

        if len(art_urls) == 0:
            return None

        for art_url in art_urls:
            art_url = BASE_URL + art_url
            yield response.follow(art_url, parse_art_page, headers=headers)

        next_url = response.css('a:contains(Next)::attr("href")').extract_first()
        if next_url is not None:
            next_url = BASE_URL + next_url
            yield response.follow(next_url, self.parse_art_pages, headers=headers)

    def parse(self, response):
        headers = response.request.headers
        tree_path = get_tree_path(response)
        categories = get_page_categories(response)

        if len(tree_path) == 0:  # if browse tree depth == 0
            categories = list(filter(lambda c: c['name'] in START_CATEGORIES, categories))

        if len(categories) == 0:
            for art_request in self.parse_art_pages(response):
                yield art_request
        else:
            for category in categories:
                name = category['name']
                url = category['url']
                headers = {'tree_path': tree_path.copy() + [name]}
                yield response.follow(url, self.parse, headers=headers)
