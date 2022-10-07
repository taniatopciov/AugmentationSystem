import cv2
import os
from tkinter import *
from tkinter import filedialog
import yaml


def parse_config_file(config_file_path='config.yml'):
    with open(config_file_path, "r") as config_file:
        config_file_content = config_file.read()
    configuration = yaml.load(config_file_content, Loader=yaml.FullLoader)

    return configuration


def select_directory():
    root = Tk()
    root.withdraw()
    directory_path = filedialog.askdirectory()

    return directory_path


def rotation_algorithm(image):
    return image


def dummy_algorithm(image):
    return image


def apply_algorithm_to_image(algorithm, image):
    if algorithm == 'rotation':
        return rotation_algorithm(image)
    elif algorithm == 'dummy':
        return dummy_algorithm(image)


def create_output_directory(output_directory_path):
    if not os.path.exists(output_directory_path):
        os.mkdir(output_directory_path)


if __name__ == '__main__':
    configurations = parse_config_file()

    images_directory = select_directory()
    output_directory_name = images_directory + '_aug'
    create_output_directory(output_directory_name)

    images = os.listdir(images_directory)

    algorithms = configurations['algorithms']

    count = 1

    for algorithm in algorithms:
        for i_name in images:
            image_path = images_directory + '/' + i_name
            image_name, image_extension = os.path.splitext(i_name)
            augmented_image_name = image_name + '_' + algorithm['name'] + '_' + str(count) + image_extension

            image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
            augmented_image = apply_algorithm_to_image(algorithm['name'], image)

            image_final_path = output_directory_name + '/' + augmented_image_name
            cv2.imwrite(image_final_path, augmented_image)
        count = count + 1
