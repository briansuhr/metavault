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
    print(parsed_xml_file)

read_metadump(metadump_file)
