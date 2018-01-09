import os
from image_details import get_xml, is_thumbnail, get_iptc_date
import find_images


image_log_file = find_images.log_directory
image_directory = find_images.image_directory


def open_image_log(image_log):
    """Opens image log text file for reading"""

    with open(image_log) as image_log:
        images = image_log.readlines()
        images = [white_space.strip() for white_space in images]

    return images


def rename_images(images):
    """Rename all images in log file with original filename from metadump.xml"""

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

    if date is False:
        return False

    else:

        date_as_string = str(date)

        # Strip out all non-date characters
        date_as_string = date_as_string.replace('[datetime.date(', '')
        date_as_string = date_as_string.replace(')]', '')

        # Split year, month, day by comma
        pure_date = [x.strip() for x in date_as_string.split(',')]

        return pure_date


def organize_images_by_date(images):
    """Creates a directory from YYYY, MM, DD values"""

    total_images = find_images.count_total_images(images)
    count = 1

    for image in images:
        print("Creating directory " + str(count) + " of " + str(total_images) + ".", end="\r")

        # Get date from image file
        date = strip_date(get_iptc_date(image))

        # If image does not have an IPTC date, create a 'No date' directory
        if date is False:
            try:
                if not os.path.exists(date_directory):
                    os.makedirs(os.path.join(image_directory, 'No date'))
            except:
                pass

        # If image has an IPTC date, create a YYYY-MM-DD directory
        else:

            year = date[0]
            month = date[1]
            day = date[2]

            # Add 0 to months and days between 1 and 9
            if len(month) == 1:
                month = str(0) + month

            if len(day) == 1:
                day = str(0) + day

            date_directory = year + '-' + month + '-' + day

            try:
                if not os.path.exists(date_directory):
                    os.makedirs(os.path.join(image_directory, date_directory))
            except:
                pass

        print(os.path.basename(image))

        count += 1


if __name__ == '__main__':
    organize_images_by_date(open_image_log(image_log_file))

