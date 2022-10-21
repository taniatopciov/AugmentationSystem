import numpy as np
import cv2


def brightness(received_image, bias):
    image = np.array(received_image, dtype=np.float64)
    image_height, image_width, image_color = image.shape

    for h in range(image_height):
        for w in range(image_width):
            for c in range(image_color):
                image[h, w, c] = np.minimum(255.0, np.maximum(0.0, image[h, w, c] + np.float64(bias)))

    image = np.array(image, dtype=np.uint8)
    return image


def contrast(received_image, gain):
    image = np.array(received_image, dtype=np.float64)
    image = image * gain
    image = image.clip(0.0, 255.0)
    image = np.array(image, dtype=np.uint8)
    return image


def gamma_correction(received_image, gamma):
    image = np.array(received_image, dtype=np.float64)
    gamma_inv = (1.0 / gamma)
    image = image / 255.0
    image = image ** gamma_inv
    image = image * 255
    image = np.array(image, dtype=np.uint8)
    return image


def compute_gaussian_kernel(size, sigma):
    kernel = np.zeros((size, size))
    center = size // 2
    for i in range(size):
        for j in range(size):
            kernel[i, j] = np.exp(-((i - center) ** 2 + (j - center) ** 2) / (2 * sigma ** 2))
    kernel = kernel / np.sum(kernel)
    return kernel


def gaussian_blur(received_image, size, sigma):
    image = np.array(received_image, dtype=np.float64)
    kernel = compute_gaussian_kernel(size, sigma)
    image = cv2.filter2D(image, -1, kernel)
    image = np.array(image, dtype=np.uint8)
    return image


# implement pixel level translation
def translation(received_image, tx, ty):
    image = np.array(received_image, dtype=np.float64)
    translation_matrix = np.float64([[1, 0, tx], [0, 1, ty]])
    image = cv2.warpAffine(image, translation_matrix, (image.shape[1], image.shape[0]))
    image = np.array(image, dtype=np.uint8)
    return image


def shearing(received_image, shx, shy):
    image = np.array(received_image, dtype=np.float64)
    shearing_matrix = np.float64([[1, shx, 0], [shy, 1, 0]])
    image = cv2.warpAffine(image, shearing_matrix, (image.shape[1], image.shape[0]))
    image = np.array(image, dtype=np.uint8)
    return image


def scaling(received_image, sx, sy):
    image = np.array(received_image, dtype=np.float64)
    scaling_matrix = np.float64([[sx, 0, 0], [0, sy, 0]])
    image = cv2.warpAffine(image, scaling_matrix, (image.shape[1], image.shape[0]))
    image = np.array(image, dtype=np.uint8)
    return image


def rotation(received_image, angle):
    image = np.array(received_image, dtype=np.float64)
    rotation_matrix = cv2.getRotationMatrix2D((image.shape[1] / 2, image.shape[0] / 2), angle, 1)
    image = cv2.warpAffine(image, rotation_matrix, (image.shape[1], image.shape[0]))
    image = np.array(image, dtype=np.uint8)
    return image
