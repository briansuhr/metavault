"""Finds all full-size images in a directory and creates a log of their paths."""

import os
import glob
from image_details import is_thumbnail, get_xml
from configparser import ConfigParser

parser = ConfigParser()
parser.read('metavault.config')

image_directory = parser.get('images', 'image_directory')
log_directory = parser.get('images', 'log_directory')


def count_total_images(images):
    image_count = 0

    for image in images:
        image_count += 1

    return image_count

def find_all_images(directory):
    """Recursively searches a photo directory for all non-thumbnail files"""

    images_found = 0
    image_files = []

    for root_directory, sub_directories, images in os.walk(directory):
        for image in images:
            if image.startswith("._"):
                continue
            elif is_thumbnail(image):
                continue
            elif image.endswith(".jpg") or image.endswith('.jpeg') or image.endswith(".tif"):
                image_path = os.path.join(root_directory, image)
                images_found += 1
                image_files.append(image_path)
            else:
                continue

        print(str(images_found) + " images found in directory: " + image_directory, end="\r")

    print("\nDone.")
    return image_files


def create_log(image_directory):
    """Creates log containing the paths of all image files"""
    image_files = open(log_directory, 'w')
    for path in find_all_images(image_directory):
        image_files.write("%s\n" % path)


if __name__ == "__main__":
    create_log(image_directory)


