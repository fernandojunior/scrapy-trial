import pytest  # noqa
from six.moves.urllib.request import urlopen
from six.moves.urllib.parse import urljoin
from scrapy.selector import Selector

BASE_URL = 'http://pstrial-2018-05-21.toscrape.com'
BROWSE_PATH = '/browse/'


def get_response(url):
    html = urlopen(url).read()
    response = Selector(text=html)
    return response


def test_browse_link_value():
    response = get_response(BASE_URL)
    browse_link = response.css('a[href*=browse]::attr("href")').extract_first()
    assert(browse_link == BROWSE_PATH)


def test_browse_subcats_num_containers():
    response = get_response(urljoin(BASE_URL, BROWSE_PATH))

    subcat_containers = response.css('#subcats div').extract()
    assert(len(subcat_containers) == 5)

    subcat_container_headers = response.css('#subcats div > a').extract()
    assert(len(subcat_container_headers) == 5)

    subcat_container_header_names = response.css('#subcats h3::text').extract()
    assert(len(subcat_container_header_names) == 5)


def test_browse_subcat_container_num_links():
    response = get_response(urljoin(BASE_URL, BROWSE_PATH))

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
