import xmltodict
import pyexiv2
import datetime

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


def get_iptc_date(image_file):
    """Reads IPTC credit from image file"""
    metadata = pyexiv2.ImageMetadata(image_file)
    metadata.read()

    datetime_exists = False

    try:
        for key in metadata.iptc_keys:
            tag = metadata[key]
            if 'Iptc.Application2.DateCreated' in key:
                datetime_exists = True
                break
    except:
        pass

    if datetime_exists:
        # Catch invalid IPTC types (e.g. 2010-12-00)
        try:
            return tag.value
        except Exception as e:
            print(e)
            pass
    else:
        return False


def get_xml(metadump_file):
    """Reads metadata from XML file in photo directory"""
    xml_file = open(metadump_file, "r").read()
    parsed_xml_file = xmltodict.parse(xml_file)

    metadata = {}

    # Get ResourceSpace image title
    for title_metadata, value in parsed_xml_file['record']['dc:title'].items():
        if title_metadata == '#text':
            try:
                metadata["Title"] = value
            except:
                pass

    # Get ResourceSpace original filename
    for original_filename in parsed_xml_file['record']['resourcespace:field']:
        for key, value in original_filename.items():
            if value == 'Original filename':
                try:
                    metadata["Original filename"] = original_filename["#text"]
                except:
                    pass

    # Get ResourceSpace image date
    for date_metadata, value in parsed_xml_file['record']['dc:date'].items():
        if date_metadata == '#text':
            try:
                metadata["Date"] = value
            except:
                pass

    # Get ResourceSpace image keywords
    for keywords_metadata in parsed_xml_file['record']['resourcespace:field']:
        for key, value in keywords_metadata.items():
            if value == 'Keywords':
                try:
                    metadata["Keywords"] = keywords_metadata["#text"]
                except:
                    pass

    # Get ResourceSpace image notes
    for notes_metadata in parsed_xml_file['record']['resourcespace:field']:
        for key, value in notes_metadata.items():
            if value == 'Notes':
                try:
                    metadata["Notes"] = notes_metadata["#text"]
                except:
                    pass

    # Get ResourceSpace image credit
    for credit_metadata in parsed_xml_file['record']['resourcespace:field']:
        for key, value in credit_metadata.items():
            if value == 'Credit':
                try:
                    metadata["Credit"] = credit_metadata["#text"]
                except:
                    pass

    return metadata


def is_thumbnail(image):
    # Use glob.iglob instead of glob.glob to avoid storing all files simultaneously.
    if 'col_' in image or 'lpr_' in image or 'pre_' in image or 'scr_' in image or 'thm_' in image:
        return True
