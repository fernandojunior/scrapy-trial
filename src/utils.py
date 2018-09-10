import re


def get_page_categories(response):
    categories = dict()

    for category_container in response.css('#subcats div'):
        category_name = category_container.css('h3::text').extract_first()
        category_link = category_container.css('a::attr("href")').extract_first()
        category_sublinks = category_container.css('li a::attr("href")').extract()
        categories[category_name] = {
            'name': category_name,
            'link': category_link,
            'sublinks': category_sublinks
        }

    return categories


def get_dimensions_in_cm(dimensions):
    width = None
    height = None
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


def parse_art_page(response, meta):
    artists = response.css('h2[itemprop=artist]::text').extract_first()

    if artists:
        artists = artists.split(';')

    dimensions = response.css('dd:contains(cm)::text').extract_first()
    width, height = get_dimensions_in_cm(dimensions)

    description = response.css('div[itemprop=description] p::text').extract_first()

    item = {
        'url': meta['url'],
        'path': meta['path'],
        'artist': artists,
        'title': response.css('h1[itemprop=name]::text').extract_first(),
        'image': response.css('img::attr("src")').extract_first(),
        'description': description,
        'width': width,
        'height': height
    }

    return ({k: v for k, v in item.items() if v is not None})
