import os
from math import log
import glob

def get_size_of_images(images):
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
        print(image_path)
    return(image_path)

def get_thumbnails_path(image_path):
    thumbnails_path = []

    thumbnail_prefixes = ['col_', 'lpr_', 'pre_', 'scr_', 'thm_']
    for prefix in thumbnail_prefixes:
        thumbnails_path.append()

def is_thumbnail(image):
    # Use glob.iglob instead of glob.glob to avoid storing all files simultaneously.
    if 'col_' in image or 'lpr_' in image or 'pre_' in image or 'scr_' in image or 'thm_' in image:
        return(True)


def pretty_size(n,pow=0,b=1024,u='B',pre=['']+[p+'i'for p in'KMGTPEZY']):
    pow,n=min(int(log(max(n*b**pow,1),b)),len(pre)-1),n*b**pow
    return "%%.%if %%s%%s"%abs(pow%(-pow-1))%(n/b**float(pow),pre[pow],u)
