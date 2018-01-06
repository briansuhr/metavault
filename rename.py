import os
from image_details import get_xml, is_thumbnail, get_iptc_date
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


def strip_date(date):
    """Strips all non-date characters from IPTC date. Returns a list of string values as YYYY, MM, DD"""

    date_as_string = str(date)

    # Strip out all non-date characters
    date_as_string = date_as_string.replace('[datetime.date(', '')
    date_as_string = date_as_string.replace(')]', '')

    # Split year, month, day by comma
    pure_date = [x.strip() for x in date_as_string.split(',')]

    print(pure_date)

    return pure_date


def rename_images_with_date(image_log):
    """Rename all images in log file with original filename from metadump.xml"""

    with open(image_log) as image_log:
        images = image_log.readlines()
        images = [white_space.strip() for white_space in images]
        total_images = find_images.count_total_images(images)

    count = 1
    for image in images:
        print("Renaming image " + str(count) + " of " + str(total_images) + ".", end="\r")

        strip_date(get_iptc_date(image))

        count += 1


if __name__ == '__main__':
    # rename_images(find_images.log_directory)
    print(rename_images_with_date(find_images.log_directory))
