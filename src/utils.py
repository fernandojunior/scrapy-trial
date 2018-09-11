import re
from config import BASE_URL


def get_tree_path(response):
    headers = response.request.headers
    return ('tree_path' in headers and headers.getlist('tree_path')) or []


def get_page_categories(response):
    categories = []

    for category_container in response.css('#subcats div'):
        category_name = category_container.css('h3::text').extract_first()
        category_url = category_container.css('a::attr("href")').extract_first()

        categories.append({
            'name': category_name,
            'url': BASE_URL + category_url
        })

    return categories


def get_dimensions_in_cm(str_dimensions):
    width = None
    height = None
    dimensions = str_dimensions
    if dimensions:
        if '(' in dimensions and ')' in dimensions:
            dimensions = re.findall(r'(?<=\().+?(?=\))', dimensions)
            dimensions = next(filter(lambda i: 'cm' in i, dimensions))

        dimensions = dimensions.replace('×', 'x')

        dimensions = re.sub('[^xX0-9\.]', '', dimensions)
        dimensions = dimensions.split('x')
        width = float(dimensions[0]) if len(dimensions) > 0 else None
        height = float(dimensions[1]) if len(dimensions) > 1 else None

    return (width, height)


def parse_art_page(response):
    request = None if type(response).__name__ is 'Selector' else response.request
    url = request.url if request is not None else None
    tree_path = get_tree_path(response) if request is not None else []

    artists = response.css('h2[itemprop=artist]::text').extract_first()
    if artists:
        artists = artists.split(';')

    dimensions = response.css('dd:contains(cm)::text').extract_first()
    width, height = get_dimensions_in_cm(dimensions)

    description = response.css('div[itemprop=description] p::text').extract_first()

    image = response.css('img::attr("src")').extract_first()
    image = image if image is None else BASE_URL + image

    item = {
        'url': url,
        'path': list(map(lambda i: i.decode('utf-8'), tree_path)),
        'artist': artists,
        'title': response.css('h1[itemprop=name]::text').extract_first(),
        'image': image,
        'description': description,
        'width': width,
        'height': height
    }

    return ({k: v for k, v in item.items() if v is not None})
