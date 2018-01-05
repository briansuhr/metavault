import os
from image_details import get_xml, is_thumbnail
import find_images


def rename_images(image_log):
    """Rename all images in log file with original filename from metadump.xml"""

    with open(image_log) as image_log:
        images = image_log.readlines()
        images = [white_space.strip() for white_space in images]
        total_images = find_images.count_total_images(images)

    count = 1
    for image in images:
        print("Renaming image " + str(count) + " of " + str(total_images) + ".", end="\r")

        image_directory = os.path.split(image)[0]
        metadump_path = os.path.join(image_directory, "metadump.xml")
        new_image_name = get_xml(metadump_path)['Original filename']
        os.rename(image, os.path.join(image_directory, new_image_name))

        count += 1

    print("\nDone.")


if __name__ == '__main__':
    rename_images(find_images.log_directory)
