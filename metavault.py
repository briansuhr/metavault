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

def write_iptc_keywords(image_file):
    metadata = pyexiv2.ImageMetadata(image_file)
    metadata.read()

    for key in metadata.iptc_keys:
         tag = metadata[key]
         if key == 'Iptc.Application2.Keywords':
             tag.value = ['puddy']
             metadata.write()

def read_metadump(metadump_file):

    xml_file = open(metadump_file, "r").read()
    parsed_xml_file = xmltodict.parse(xml_file)

    # Get ResourceSpace image title
    for title_metadata, value in parsed_xml_file['record']['dc:title'].items():
        if title_metadata == '#text':
            print("TITLE")
            try:
                print(value)
            except:
                print("Title field empty")
                continue

    # Get ResourceSpace image keywords
    for metadata in parsed_xml_file['record']['resourcespace:field']:
        for key, value in metadata.items():
            if value == 'Keywords':
                print("\n")
                print("KEYWORDS")
                try:
                    print(metadata['#text'])
                except:
                    print("Keywords field empty")
                    continue

    # Get ResourceSpace image notes
    for metadata in parsed_xml_file['record']['resourcespace:field']:
        for key, value in metadata.items():
            if value == 'Notes':
                print("\n")
                print("NOTES")
                try:
                    print(metadata['#text'])
                except:
                    print("Notes field empty")
                    continue

read_metadump(metadump_file)
