import re


def parse_art_item(response, meta):
    artists = response.css('h2[itemprop=artist]::text').extract_first()

    if artists:
        artists = artists.split(';')
        artists = list(map(lambda i: i.split(': ')[1], artists))

    image_dimension = response.css('dd:contains(cm)::text').extract_first()
    image_dimension = re.findall(r'(?<=\().+?(?=\))', image_dimension)
    image_dimension = next(filter(lambda i: 'cm' in i, image_dimension))
    image_dimension = re.sub('[^xX0-9\.]', '', image_dimension)
    image_dimension = list(map(float, image_dimension.split('x')))

    description = response.css('div[itemprop=description] p::text').extract_first()

    item = {
        'url': meta['url'],
        'path': meta['path'],
        'artist': artists,
        'title': response.css('h1[itemprop=name]::text').extract_first(),
        'image': response.css('img::attr("src")').extract_first(),
        'description': description,
        'width': image_dimension[0] if len(image_dimension) >= 2 else None,
        'height': image_dimension[1] if len(image_dimension) >= 2 else None
    }

    return ({k: v for k, v in item.items() if v is not None})
