def get_size_of_all_images():
    list_of_images = open('image_files.txt', 'r')
    images = list_of_images.readlines())
    for image in images:
        print(image[0])
    list_of_images.close()

get_size_of_all_images()
