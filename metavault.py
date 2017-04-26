import os
import pyexiv2

photo_directory = 'resourcespace'

def print_all_files():
    for sub_directory, directorys, files in os.walk(photo_directory):
        for file in files:
            print(os.path.join(sub_directory, file))

def read_iptc_tags(image_file):
    metadata = pyexiv2.ImageMetadata(image_file)
    metadata.read()

    for key in metadata.iptc_keys:
        tag = metadata[key]
        print(tag)

read_iptc_tags('9944_8640aa4d8fb8168.jpg')
