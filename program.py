import cv2
import os
from tkinter import *
from tkinter import filedialog
import yaml

from algorithms import *


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


def create_output_directory(output_directory_path):
    if not os.path.exists(output_directory_path):
        os.mkdir(output_directory_path)


def apply_algorithm_to_image(image, algorithm, parameters):
    if algorithm == 'Brightness':
        return brightness(image, parameters[0]['value'])
    elif algorithm == 'Contrast':
        return contrast(image, parameters[0]['value'])
    elif algorithm == 'Gamma Correction':
        return gamma_correction(image, parameters[0]['value'])
    elif algorithm == 'Gaussian Blur':
        return gaussian_blur(image, parameters[0]['value'], parameters[1]['value'])
    elif algorithm == 'Translation':
        return translation(image, parameters[0]['value'], parameters[1]['value'])
    elif algorithm == "Shearing":
        return shearing(image, parameters[0]['value'], parameters[1]['value'])
    elif algorithm == 'Scaling':
        return scaling(image, parameters[0]['value'], parameters[1]['value'])
    elif algorithm == 'Rotation':
        return rotation(image, parameters[0]['value'])
    else:
        print('Algorithm \"' + algorithm + '\" not supported')
        return None


def main():
    configurations = parse_config_file()
    images_directory = select_directory()
    output_directory_name = images_directory + '_aug'
    create_output_directory(output_directory_name)
    images = os.listdir(images_directory)
    algorithms = configurations['algorithms']

    count = 1

    for i_name in images:
        image_path = images_directory + '/' + i_name
        image_name, image_extension = os.path.splitext(i_name)

        for algorithm in algorithms:
            augmented_image_name = image_name + '_' + algorithm['name'] + '_' + str(count) + image_extension

            image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

            parameters = []
            for parameter in algorithm['parameters']:
                parameters.append(parameter)

            # augmented_image = apply_algorithm_to_image(image, algorithm['name'], algorithm['parameters'][0]['value'])
            augmented_image = apply_algorithm_to_image(image, algorithm['name'], parameters)

            image_final_path = output_directory_name + '/' + augmented_image_name

            if augmented_image is not None:
                if image_final_path is not None:
                    cv2.imwrite(image_final_path, augmented_image)

        count = count + 1


if __name__ == '__main__':
    main()
