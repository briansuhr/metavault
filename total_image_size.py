import os
from math import log

def get_size_of_all_images():
    list_of_images = open('image_files.txt', 'r')
    images = list_of_images.readlines()

    images_found = 0
    total_size = 0

    for image in images:
        image_path = str(get_full_image_path(image))
        images_found += 1
        total_size += (os.path.getsize(image_path))
        pretty_total_size = pretty_size(total_size)
        print(str("Images found: ") + str(images_found) + " Total size: " + str(pretty_total_size), end="\r")

    list_of_images.close()

def get_full_image_path(image_path):
    characters = "[]'"
    for character in characters:
        if character in image_path:
            image_path = image_path.replace(character, "")
            image_path = image_path.replace(',', '/')
            image_path = image_path.replace(' ', '')
            image_path = image_path.strip()
    return(image_path)

def pretty_size(n,pow=0,b=1024,u='B',pre=['']+[p+'i'for p in'KMGTPEZY']):
    pow,n=min(int(log(max(n*b**pow,1),b)),len(pre)-1),n*b**pow
    return "%%.%if %%s%%s"%abs(pow%(-pow-1))%(n/b**float(pow),pre[pow],u)

get_size_of_all_images()
