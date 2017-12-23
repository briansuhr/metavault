from shutil import copyfile
import os


def count_total_images(images):
    image_count = 0

    for image in images:
        image_count += 1

    return image_count

def extract_images(image_log):
    """Uses the image log to move all full-size images to a new directory"""

    with open(image_log) as image_log:
        images = image_log.readlines()
        images = [white_space.strip() for white_space in images]
        total_images = count_total_images(images)

    count = 1
    for image in images:
        print("Copying image " + str(count) + " of " + str(total_images) + ".", end="\r")
        base_image_path = os.path.basename(image)
        extraction_directory = os.path.join("extract", base_image_path)
        copyfile(image, extraction_directory)
        count += 1

    print("\nDone.")


if __name__ == "__main__":
    extract_images("log/image_files.txt")