import math
import sys
from io import BytesIO

import requests
from PIL import Image

from utilities import get_object, get_ll_spn

search_api_server = "https://search-maps.yandex.ru/v1/"
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
map_api_server = "https://static-maps.yandex.ru/v1"


def get_distance(point1, point2):
    lon1, lat1 = point1
    lon2, lat2 = point2
    meters = 1000
    radius_latitude = math.radians((lat1 + lat2) / 2)
    lat_lon_factor = math.cos(radius_latitude)
    dx = abs(lon1 - lon2) * meters * lat_lon_factor
    dy = abs(lat1 - lat2) * 1000
    distance = math.sqrt(dx ** 2 + dy ** 2)
    return round(distance, 2)


try:
    toponym_to_find = " ".join(sys.argv[1:])
except RuntimeError:
    print('Неверный адрес')
    sys.exit()
toponym_object = get_object(toponym_to_find)
toponym_points = list(map(float, toponym_object["Point"]["pos"].split()))
address_ll, spn = get_ll_spn(toponym_object)

search_params = {
    "apikey": "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3",
    "text": "аптека",
    "lang": "ru_RU",
    "ll": address_ll,
    "type": "biz"
}

response = requests.get(search_api_server, params=search_params)
if not response:
    pass
json_response = response.json()

organization = json_response["features"][0]
org_hours = organization["properties"]["CompanyMetaData"]['Hours']['text']
org_name = organization["properties"]["CompanyMetaData"]["name"]
org_address = organization["properties"]["CompanyMetaData"]["address"]
point = organization["geometry"]["coordinates"]
org_point = f"{point[0]},{point[1]}"
delta = "0.005"
apikey = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"
center_lat = (toponym_points[0] + point[0]) / 2
center_lon = (toponym_points[1] + point[1]) / 2

map_params = {
    "ll": f"{center_lat},{center_lon}",
    "spn": ",".join([delta, delta]),
    "apikey": apikey,
    "pt": "~".join(["{0},pm2dgl".format(org_point), address_ll])
}
response = requests.get(map_api_server, params=map_params)
print(f"Название: {org_name}.\n"
      f"График работы: {org_hours}.\n"
      f"Расстояние до аптеки: ~{get_distance(toponym_points, point)} км.")
im = BytesIO(response.content)
opened_image = Image.open(im)
opened_image.show()
