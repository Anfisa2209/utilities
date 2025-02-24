from utilities import *
toponym_to_find = " ".join(sys.argv[1:])
toponym_object = get_object(toponym_to_find)
ll, spn = get_ll_spn(toponym_object)
image_file = get_static_api_image(ll, spn)
with open('map.png', 'wb') as file:
    file.write(image_file)
show_image('map.png')