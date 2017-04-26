import os
import pyexiv2
import xmltodict
from collections import namedtuple

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

def read_metadump(metadump_file):

    xml_file = open(metadump_file, "r").read()
    parsed_xml_file = xmltodict.parse(xml_file)

    metadata = []

    # Get ResourceSpace image title
    for title_metadata, value in parsed_xml_file['record']['dc:title'].items():
        if title_metadata == '#text':
            try:
                '#text' in title_metadata
                metadata.append({'Title': value})
            except:
                pass

    # Get ResourceSpace image date
    for date_metadata, value in parsed_xml_file['record']['dc:date'].items():
        if date_metadata == '#text':
            try:
                '#text' in date_metadata
                metadata.append({'Date': value})
            except:
                pass

    # Get ResourceSpace image keywords
    for image_metadata in parsed_xml_file['record']['resourcespace:field']:
        for key, value in image_metadata.items():
            if value == 'Keywords':
                try:
                    'Keywords' in image_metadata
                    metadata.append({'Keywords': image_metadata['#text']})
                except:
                    pass

    # Get ResourceSpace image notes
    for notes_metadata in parsed_xml_file['record']['resourcespace:field']:
        for key, value in notes_metadata.items():
            if value == 'Notes':
                try:
                    'Notes' in image_metadata
                    metadata.append({'Notes': notes_metadata['#text']})
                except:
                    pass

    # Get ResourceSpace image credit
    for credit_metadata in parsed_xml_file['record']['resourcespace:field']:
        for key, value in credit_metadata.items():
            if value == 'Credit':
                try:
                    'Credit' in credit_metadata
                    metadata.append({'Credit': credit_metadata['#text']})
                except:
                    pass

    print(metadata)
    return(metadata)

def write_iptc_keywords(image_file):
    metadata = pyexiv2.ImageMetadata(image_file)
    metadata.read()

    #Get metadump file

    for key in metadata.iptc_keys:
         tag = metadata[key]
         if key == 'Iptc.Application2.Keywords':
             tag.value = ['puddy']
             metadata.write()

read_metadump(metadump_file)
