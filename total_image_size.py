def get_size_of_all_images():
    list_of_images = open('image_files.txt', 'r')
    print(list_of_images.readlines())
    list_of_images.close()

get_size_of_all_images()
