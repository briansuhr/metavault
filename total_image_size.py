def get_size_of_all_images():
    list_of_images = open('image_files.txt', 'r')
    images = list_of_images.readlines()
    images.close()

get_size_of_all_images()
