import os
from photo_details import get_xml, is_thumbnail

def rename_photos():
    """Renames photos in directory with XML metadump information"""

    photo_directory = "photos/7_17dae6df35e1463/"
    for photo in os.listdir(photo_directory):
        if photo.startswith("._"):
            continue
        elif is_thumbnail(photo):
            continue
        elif photo.endswith(".jpg") or photo.endswith('.jpeg') or photo.endswith(".tif"):
            os.rename(photo_directory + photo, photo_directory + get_xml(photo_directory + "metadump.xml")['Original filename'])
        else:
            continue

if __name__ == '__main__':

    rename_photos()
