import os
from math import log
from metavault import get_image_files
import glob

def get_size_of_images(images):

    total_file_size = 0

    print('\n')
    print("Calculating file size...")
    for image in images:
        image_path = str(image[0]) + '/' + str(image[1])
        file_size = os.path.getsize(image_path)
        total_file_size += file_size
        print(pretty_size(total_file_size), end="\r")

    print("\n")
    print("Total size: " + str(pretty_size(total_file_size)))
    return(total_file_size)

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


def pretty_size(n,pow=0,b=1024,u='B',pre=['']+[p+'i'for p in'KMGTPEZY']):
    pow,n=min(int(log(max(n*b**pow,1),b)),len(pre)-1),n*b**pow
    return "%%.%if %%s%%s"%abs(pow%(-pow-1))%(n/b**float(pow),pre[pow],u)


get_size_of_images(get_image_files("thumbnail"))
