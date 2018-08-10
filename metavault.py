import os
import pyexiv2
from shutil import copyfile
from configparser import ConfigParser

parser = ConfigParser()
parser.read('metavault.config')

image_log = parser.get('images', 'log_directory')


def write_iptc_data():

    count = 0

    print("Writing metadata to images...")

    with open(image_log) as image_log_file: 
        images = image_log_file.readlines()

        for image in images:
            print("This image " + image)

            # Look for metadump file
            metadump_file = (str(os.path.dirname(image)) + '/metadump.xml')
            print("metadump file " + metadump_file)
            image_filepath = str(image[0]) + "/" + str(image[1])
            print("image filepath " + image_filepath)

            try:
                os.path.isfile(metadump_file)
            except:
                print("No metadump file found for" + str(image[1]) + ".")
                count += 1
                continue

            image_fields = pyexiv2.ImageMetadata(image_filepath)

            try:
                image_fields.read()
            except:
                print("Failed to open image " + str(image_filepath))

                continue

            try:
                metadata = read_metadump(metadump_file)
            except:
                print("Failed to open metadump file for image " + str(image_filepath))
                continue

            # Write keywords
            try:
                if metadata.get('Keywords'):
                    key = 'Iptc.Application2.Keywords'
                    value = metadata.get('Keywords')
                    image_fields[key] = [value]
            except:
                pass

            # Write headline
            try:
                if metadata.get('Title'):
                    # Needs to be IPTC Byline. Using Creator causes an error.
                    key = 'Iptc.Application2.Headline'
                    value = metadata.get('Title')
                    image_fields[key] = [value]
            except:
                pass

            # Write credit
            try:
                if metadata.get('Credit'):
                    # Needs to be IPTC Byline. Using Creator causes an error.
                    key = 'Iptc.Application2.Byline'
                    value = metadata.get('Byline')
                    image_fields[key] = [value]
            except:
                pass

            try:
                print("(" + str(int(count / len(all_image_files) * 100)) + "%) Writing metadata to image " + str(
                    count) + " of " + str(len(all_image_files)), end="\r")
                image_fields.write()
                count += 1

            except:
                print("Failed to add metadata to " + str(image_file[1]))
                count += 1
                continue

    print("\n")
    print("Done.")

def copy_images_to_new_directory():
    images_to_move = get_all_image_files()
    image_destination_directory = "images_with_metadata"

    count = 0
    for image in images_to_move:
        count += 1
        image_source = str(image[0]) + "/" + str(image[1])
        image_destination_filepath = image_destination_directory + "/" + str(image[1])
        print(
        "(" + str(int(count / len(images_to_move) * 100)) + "%) Copying image " + str(count) + " of " + str(
            len(images_to_move)) + " to /" + image_destination_directory, end="\r")
        copyfile(image_source, image_destination_filepath)

    print("Done.")

write_iptc_data()
