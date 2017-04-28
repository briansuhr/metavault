import os
import pyexiv2
import xmltodict
import glob
from shutil import copyfile


def get_iptc_keywords(image_file):
    metadata = pyexiv2.ImageMetadata(image_file)
    metadata.read()

    for key in metadata.iptc_keys:
        tag = metadata[key]
        if key == 'Iptc.Application2.Keywords':
            print(tag.value)

def get_iptc_credit(image_file):
    metadata = pyexiv2.ImageMetadata(image_file)
    metadata.read()

    for key in metadata.iptc_keys:
        tag = metadata[key]
        print(str(key)+ str(tag.value))
        if key == 'Iptc.Application2.Credit':
            print(tag.value)

def read_metadump(metadump_file):

    xml_file = open(metadump_file, "r").read()
    parsed_xml_file = xmltodict.parse(xml_file)

    metadata = {}

    # Get ResourceSpace image title
    for title_metadata, value in parsed_xml_file['record']['dc:title'].items():
        if title_metadata == '#text':
            try:
                '#text' in title_metadata
                metadata["Title"] = value
            except:
                pass

    # Get ResourceSpace image date
    for date_metadata, value in parsed_xml_file['record']['dc:date'].items():
        if date_metadata == '#text':
            try:
                '#text' in date_metadata
                metadata["Date"] = value
            except:
                pass

    # Get ResourceSpace image keywords
    for keywords_metadata in parsed_xml_file['record']['resourcespace:field']:
        for key, value in keywords_metadata.items():
            if value == 'Keywords':
                try:
                    'Keywords' in keywords_metadata
                    metadata["Keywords"] = keywords_metadata["#text"]
                except:
                    pass

    # Get ResourceSpace image notes
    for notes_metadata in parsed_xml_file['record']['resourcespace:field']:
        for key, value in notes_metadata.items():
            if value == 'Notes':
                try:
                    'Notes' in image_metadata
                    metadata["Notes"] = notes_metadata["#text"]
                except:
                    pass

    # Get ResourceSpace image credit
    for credit_metadata in parsed_xml_file['record']['resourcespace:field']:
        for key, value in credit_metadata.items():
            if value == 'Credit':
                try:
                    'Credit' in credit_metadata
                    metadata["Credit"] = credit_metadata["#text"]
                except:
                    pass

    return(metadata)

def is_thumbnail(image):
    # Use glob.iglob instead of glob.glob to avoid storing all files simultaneously.
    if 'col_' in image or 'lpr_' in image or 'pre_' in image or 'scr_' in image or 'thm_' in image:
        return(True)

def get_image_files(image_type):
    image_directory = 'filestorebk'
    number_of_images = 0
    image_files = []

    for image in glob.iglob(image_directory + '/**/*.jpg', recursive=True):
        # Use glob.iglob instead of glob.glob to avoid storing all files simultaneously.
        if image_type == "original" and is_thumbnail(image) == False:
            number_of_images += 1

            # Split up directory and image basename
            image_file_location = []
            image_directory = os.path.dirname(image)
            image_basename = os.path.basename(image)

            image_file_location.append(image_directory)
            image_file_location.append(image_basename)

            image_files.append(image_file_location)
            image_file_location = []

            print(str(number_of_images) + " full size images found.", end="\r")

        elif image_type == "thumbnail" and is_thumbnail(image) == True:
            number_of_images += 1

            # Split up directory and image basename
            image_file_location = []
            image_directory = os.path.dirname(image)
            image_basename = os.path.basename(image)

            image_file_location.append(image_directory)
            image_file_location.append(image_basename)

            image_files.append(image_file_location)
            image_file_location = []

            print(str(number_of_images) + " thumbnail images found.", end="\r")

    return(image_files)

def images_log(image_file_list):
    image_files = open('image_files.txt', 'w')
    for image_file in image_file_list:
        image_files.write("%s\n" % image_file)

def write_iptc_data():

    count = 0

    all_image_files = get_all_image_files()
    images_log(all_image_files)

    print("Writing metadata to images...")

    for image_file in all_image_files:

        # Look for metadump file
        metadump_file = (str(image_file[0]) + '/metadump.xml')
        image_filepath = str(image_file[0]) + "/" + str(image_file[1])

        try:
            os.path.isfile(metadump_file)
        except:
            print("No metadump file found for" + str(image_file[1]) + ".")
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
            print("(" + str(int(count/len(all_image_files) * 100)) + "%) Writing metadata to image " + str(count) + " of " + str(len(all_image_files)), end="\r")
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
        print("(" + str(int(count/len(images_to_move) * 100)) + "%) Copying image " + str(count) + " of " + str(len(images_to_move)) + " to /" + image_destination_directory, end="\r")
        copyfile(image_source, image_destination_filepath)

    print("Done.")
