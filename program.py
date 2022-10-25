import cv2
import os
from tkinter import *
from tkinter import filedialog
import yaml

from algorithms import *


def select_directory():
    root = Tk()
    root.withdraw()
    directory_path = filedialog.askdirectory(initialdir="/Facultate/Master/Anul I/FCV/First Project", title="Select images directory")
    return directory_path


def select_config_file():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(initialdir="/Facultate/Master/Anul I/FCV/First Project", title="Select configuration file")
    return file_path


def parse_config_file(config_file_path):
    with open(config_file_path, "r") as config_file:
        config_file_content = config_file.read()
    configuration = yaml.load(config_file_content, Loader=yaml.FullLoader)
    return configuration


def create_output_directory(output_directory_path):
    if not os.path.exists(output_directory_path):
        os.mkdir(output_directory_path)


def compute_image_name(image_name, algorithm_name, count, image_extension):
    return image_name + '_' + algorithm_name + '_' + str(count) + image_extension


def get_algorithm_parameters(algorithm):
    parameters = []
    for parameter in algorithm['parameters']:
        parameters.append(parameter)
    return parameters


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
    config_file_path = select_config_file()
    configurations = parse_config_file(config_file_path)
    images_directory = select_directory()
    output_directory_name = images_directory + '_aug'
    create_output_directory(output_directory_name)
    images = os.listdir(images_directory)
    algorithms = configurations['algorithms']

    count = 1

    for i_name in images:
        image_path = images_directory + '/' + i_name
        image_name, image_extension = os.path.splitext(i_name)

        if image_extension == '.jpg':

            image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

            if image is not None:

                for algorithm in algorithms:

                    if algorithm['name'] == 'Chain Processing':

                        chain_algorithms = algorithm['parameters'][0]['value']
                        augmented_image_name = image_name
                        augmented_image = image

                        for chain_algorithm in chain_algorithms:
                            algorithm_name = chain_algorithm['name']
                            augmented_image_name = augmented_image_name + '_' + algorithm_name
                            algorithm_parameters = get_algorithm_parameters(chain_algorithm)
                            augmented_image = apply_algorithm_to_image(augmented_image, algorithm_name,
                                                                       algorithm_parameters)

                        augmented_image_name = augmented_image_name + image_extension

                    else:
                        augmented_image_name = compute_image_name(image_name, algorithm['name'], count, image_extension)

                        augmented_image = apply_algorithm_to_image(image, algorithm['name'],
                                                                   get_algorithm_parameters(algorithm))

                    image_final_path = output_directory_name + '/' + augmented_image_name

                    if augmented_image is not None:
                        if image_final_path is not None:
                            cv2.imwrite(image_final_path, augmented_image)

                    count = count + 1


if __name__ == '__main__':
    main()
