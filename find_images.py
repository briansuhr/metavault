import os
import glob
from image_details import is_thumbnail, get_xml

def find_all_images(image_directory):
    """Recursively searches a photo directory for all non-thumbnail files"""

    images_found = 0
    image_files = []

    for root_directory, sub_directories, images in os.walk(image_directory):
        for image in images:
            if image.startswith("._"):
                continue
            elif is_thumbnail(image):
                continue
            elif image.endswith(".jpg") or image.endswith('.jpeg') or image.endswith(".tif"):
                image_path = os.path.join(root_directory, image)
                images_found += 1
                image_files.append(image_path)
            else:
                continue

        print(str(images_found) + " images found.", end="\r")

    print("\nDone.")
    return image_files


def create_log(image_directory):
    """Creates log containing the paths of all image files"""
    image_files = open('log/image_files.txt', 'w')
    for path in find_all_images(image_directory):
        image_files.write("%s\n" % path)


if __name__ == "__main__":
    create_log("photos/")
