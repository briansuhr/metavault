import os
import xmltodict


def read_metadump(metadump_file):
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


def rename_photos():
    """Renames photos in directory with XML metadump information"""

    photo_directory = "photos/7_17dae6df35e1463/"
    for photo in os.listdir(photo_directory):
        if photo.startswith("._"):
            continue
        elif "col_" in photo or "pre_" in photo or "scr_" in photo or "thm_" in photo:
            continue
        elif photo.endswith(".jpg") or photo.endswith('.jpeg') or photo.endswith(".tif"):
            os.rename(photo_directory + photo, photo_directory + read_metadump(photo_directory + "metadump.xml")['Original filename'])
        else:
            continue

rename_photos()
