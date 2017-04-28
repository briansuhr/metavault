
def get_size_of_all_images():
    list_of_images = open('image_files.txt', 'r')
    images = list_of_images.readlines()
    for image in images:
        image_path = replace_characters(image)
        print(image_path)
    list_of_images.close()


def replace_characters(image_path):
    characters = "[]'"
    for character in characters:
        if character in image_path:
            image_path = image_path.replace(character, "")
    return(image_path)

get_size_of_all_images()
