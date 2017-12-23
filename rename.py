import os
from image_details import get_xml, is_thumbnail


def rename_all_images(image_directory):
    """Recursively rename all non-thumbnail images in an image directory"""

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

    rename_all_images("photos/")

