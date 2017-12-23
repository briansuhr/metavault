from shutil import copyfile
import os


def count_total_images(image_log):
    image_count = 0
    with open(image_log) as image_log:
        images = image_log.readlines()
        for image in images:
            count += 1

    return image_count

def extract_images(image_log):
    """Uses the image log to move all full-size images to a new directory"""

    with open(image_log) as image_log:
        images = image_log.readlines()
        images = [white_space.strip() for white_space in images]

    for image in images:
        base_image_path = os.path.basename(image)
        extraction_directory = os.path.join("extract", base_image_path)

        copyfile(image, extraction_directory)


if __name__ == "__main__":
    print(count_total_images("log/image_files.txt"))
    extract_images("log/image_files.txt")