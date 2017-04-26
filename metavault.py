import os
import pyexiv2
import xmltodict

photo_directory = 'resourcespace'
image_file = '9944_8640aa4d8fb8168.jpg'
metadump_file = 'metadump.xml'

def print_all_files():
    for sub_directory, directorys, files in os.walk(photo_directory):
        for file in files:
            print(os.path.join(sub_directory, file))

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

def write_iptc_data(image_file):
    image_fields = pyexiv2.ImageMetadata(image_file)
    image_fields.read()

    metadata = read_metadump(metadump_file)
    print(metadata)

    # Write keywords
    if metadata.get('Keywords'):
        key = 'Iptc.Application2.Keywords'
        value = metadata.get('Keywords')
        image_fields[key] = [value]

    # Write headline
    if metadata.get('Title'):
        # Needs to be IPTC Byline. Using Creator causes an error.
        key = 'Iptc.Application2.Headline'
        value = metadata.get('Title')
        image_fields[key] = [value]

    # Write credit
    if metadata.get('Credit'):
        # Needs to be IPTC Byline. Using Creator causes an error.
        key = 'Iptc.Application2.Byline'
        value = metadata.get('Byline')
        image_fields[key] = [value]

    image_fields.write()

write_iptc_data(image_file)
get_iptc_credit(image_file)
