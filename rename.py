import os
from photo_details import get_xml, is_thumbnail

def rename_photos():
    """Renames photos in directory with XML metadump information"""

    image_directory = "photos/7_17dae6df35e1463/"
    for image in os.listdir(image_directory):
        if image.startswith("._"):
            continue
        elif is_thumbnail(image):
            continue
        elif image.endswith(".jpg") or image.endswith('.jpeg') or image.endswith(".tif"):
            os.rename(image_directory + image, image_directory + get_xml(image_directory + "metadump.xml")['Original filename'])
        else:
            continue

if __name__ == '__main__':

    rename_photos()
