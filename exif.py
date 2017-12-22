import pyexiv2
"""Reads EXIF data from image file"""

def get_iptc_keywords(image_file):
    """Reads IPTC keywords from image file"""
    metadata = pyexiv2.ImageMetadata(image_file)
    metadata.read()

    for key in metadata.iptc_keys:
        tag = metadata[key]
        if key == 'Iptc.Application2.Keywords':
            print(tag.value)


def get_iptc_credit(image_file):
    """Reads IPTC credit from image file"""
    metadata = pyexiv2.ImageMetadata(image_file)
    metadata.read()

    for key in metadata.iptc_keys:
        tag = metadata[key]
        print(str(key) + str(tag.value))
        if key == 'Iptc.Application2.Credit':
            print(tag.value)
