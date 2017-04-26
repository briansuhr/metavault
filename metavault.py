import os
import pyexiv2
import xmltodict
import glob
import os
import math

image_directory = 'resourcespace'
image_file = '9944_8640aa4d8fb8168.jpg'

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

def get_all_image_files():
    number_of_images = 0
    image_files = []

    for image in glob.iglob('resourcespace/**/*.jpg', recursive=True):
        # Use glob.iglob instead of glob.glob to avoid storing all files simultaneously.
        if 'col_' not in image and 'lpr_' not in image and 'pre_' not in image and 'scr_' not in image and 'thm_' not in image:
            number_of_images += 1

            # Split up directory and image basename
            image_file_location = []
            image_directory = os.path.dirname(image)
            image_basename = os.path.basename(image)

            image_file_location.append(image_directory)
            image_file_location.append(image_basename)

            image_files.append(image_file_location)
            image_file_location = []

            print(str(number_of_images) + " images found.", end="\r")

    return(image_files)

def write_iptc_data():

    count = 0

    all_image_files = get_all_image_files()

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
        image_fields.read()

        metadata = read_metadump(metadump_file)

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

    print("Done.")

write_iptc_data()
