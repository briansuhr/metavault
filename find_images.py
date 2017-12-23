import os
import glob
from image_details import is_thumbnail, get_xml


def find_image_files(image_type):
    image_directory = 'filestorebk'
    number_of_images = 0
    image_files = []

    for image in glob.iglob(image_directory + '/**/*.jpg', recursive=True):

        # Use glob.iglob instead of glob.glob to avoid storing all files simultaneously.

        if image_type == "original" and not is_thumbnail(image):
            number_of_images += 1

            get_xml(image)

            print(str(number_of_images) + " full size images found.", end="\r")

        elif image_type == "thumbnail" and is_thumbnail(image):
            number_of_images += 1

            # Split up directory and image basename
            image_file_location = []
            image_directory = os.path.dirname(image)
            image_basename = os.path.basename(image)

            image_file_location.append(image_directory)
            image_file_location.append(image_basename)

            image_files.append(image_file_location)

            print(str(number_of_images) + " thumbnail images found.", end="\r")

        return image_files