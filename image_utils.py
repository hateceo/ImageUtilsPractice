import cv2
import numpy as np


def extract_channel(image, channel):
    """Извлечение цветового канала"""
    if image is None:
        return None

    channels = {
        'r': lambda img: cv2.merge([np.zeros_like(img[:, :, 0]), np.zeros_like(img[:, :, 1]), img[:, :, 2]]),
        'g': lambda img: cv2.merge([np.zeros_like(img[:, :, 0]), img[:, :, 1], np.zeros_like(img[:, :, 2])]),
        'b': lambda img: cv2.merge([img[:, :, 0], np.zeros_like(img[:, :, 1]), np.zeros_like(img[:, :, 2])])
    }

    if channel not in channels:
        return None

    return channels[channel](image)


def process_red_mask(image, threshold):
    """Создание маски красных областей"""
    if image is None:
        return None

    red = image[:, :, 2]
    mask = (red > threshold).astype(np.uint8) * 255
    return cv2.merge([mask, mask, mask])