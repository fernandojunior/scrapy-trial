import os
import sys
import pytest  # noqa
from six.moves.urllib.request import urlopen
from six.moves.urllib.parse import urljoin
from scrapy.selector import Selector

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(TEST_DIR, os.pardir))
sys.path.insert(0, PROJECT_DIR + '/art_spider')
from art_spider.spiders.arts.utils import parse_art_page, get_dimensions_in_cm  # noqa

BASE_URL = 'http://pstrial-2018-05-21.toscrape.com'
BROWSE_PATH = '/browse/'
BROWSE_URL = urljoin(BASE_URL, BROWSE_PATH)


def follow(absolute_url, callback):
    response = get_response(absolute_url)
    return callback(response)


def get_response(url):
    html = urlopen(url).read()
    response = Selector(text=html)
    return response


def test_browse_link_value():
    response = get_response(BASE_URL)
    browse_link = response.css('a[href*=browse]::attr("href")').extract_first()
    assert(browse_link == BROWSE_PATH)


def test_browse_subcats_num_containers():
    response = get_response(BROWSE_URL)

    subcat_containers = response.css('#subcats div').extract()
    assert(len(subcat_containers) == 5)

    subcat_container_headers = response.css('#subcats div > a').extract()
    assert(len(subcat_container_headers) == 5)

    subcat_container_header_names = response.css('#subcats h3::text').extract()
    assert(len(subcat_container_header_names) == 5)


def test_browse_subcat_container_num_links():
    response = get_response(BROWSE_URL)

    num_links_by_container = {
        'Fragrant Ladies': 0,
        'In Sunsh': 0,
        'Qing Japanese': 5,
        'Une Tete': 8,
        'Summertime': 4
    }

    for container in response.css('#subcats div'):
        header_name = container.css('h3::text').extract_first()
        assert(header_name in num_links_by_container.keys())
        links = container.css('li a').extract()
        assert(num_links_by_container[header_name] == len(links))


def test_get_dimentions_in_cm():
    width, height = get_dimensions_in_cm('22 x 47 cm')
    assert(width == 22 and height == 47)
    width, height = get_dimensions_in_cm('Overall: 3 3/4 in. (9.53 cm)')
    assert(width == 9.53 and height is None)


def test_parse_firt_page_items_from_insunsh_cat():
    url = 'http://pstrial-2018-05-21.toscrape.com/browse/insunsh'
    response = get_response(url)
    item_paths = response.css('a[href*=item]::attr("href")').extract()

    assert(len(item_paths) == 10)

    for item_path in item_paths:
        url = BASE_URL + item_path
        item = follow(url, callback=parse_art_page)
        assert(len(item.values()) > 0)
