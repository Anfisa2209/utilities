import sys
from io import BytesIO

import requests
from PIL import Image

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
geocoder_params = {
    "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
    "format": "json"}


def get_object(address):
    geocoder_params['geocode'] = address
    response = requests.get(geocoder_api_server, geocoder_params)
    if response:
        json_response = response.json()
    else:
        raise RuntimeError('Ошибка выполнения запроса.')
    feature = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
    return feature if feature else None


def get_ll_spn(toponym: dict):
    object_ll = ','.join(toponym['Point']['pos'].split())
    envelope = toponym['boundedBy']['Envelope']
    left, bottom = envelope['lowerCorner'].split()
    right, top = envelope['upperCorner'].split()
    dx = abs(float(left) - float(right)) / 2
    dy = abs(float(top) - float(bottom)) / 2
    object_spn = f"{dx},{dy}"
    return object_ll, object_spn


def get_static_api_image(object_ll, object_spn):
    map_params = {
        "ll": object_ll,
        "spn": object_spn,
        "pt": object_ll
    }
    map_api_server = "https://static-maps.yandex.ru/1.x/?l=map"
    response = requests.get(map_api_server, params=map_params)
    if response:
        # return response.content
        show_image(response.content)
    else:

        raise RuntimeError('Ошибка выполнения запроса.')


def show_image(content):
    im = BytesIO(content)
    image = Image.open(im)
    image.show()


if __name__ == '__main__':
    toponym_to_find = " ".join(sys.argv[1:])
    toponym_object = get_object(toponym_to_find)
    ll, spn = get_ll_spn(toponym_object)
    image_file = get_static_api_image(ll, spn)
    with open('map.png', 'wb') as file:
        file.write(image_file)
    show_image('map.png')
