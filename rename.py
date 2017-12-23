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

def list_all_photos():
    image_directory = "photos/"
    for root_directory, sub_directories, images in os.walk(image_directory):
        for image in images:
            if image.startswith("._"):
                continue
            elif is_thumbnail(image):
                continue
            elif image.endswith(".jpg") or image.endswith('.jpeg') or image.endswith(".tif"):
                image_path = os.path.join(root_directory, image)
                metadump_file_location = os.path.join(root_directory, "metadump.xml")
                original_filename = get_xml(metadump_file_location)['Original filename']
                os.rename(image_path, os.path.join(root_directory, original_filename))
            else:
                continue

if __name__ == '__main__':

    list_all_photos()
