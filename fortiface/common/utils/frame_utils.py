import cv2
import numpy as np


def sharpen_frame(frame):
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])

    # Sharpen the image
    sharpened_image = cv2.filter2D(frame, -1, kernel)
    return sharpened_image


def resize_frame(frame, size=(200, 200), interpolation=cv2.INTER_AREA):
    return cv2.resize(frame, size, interpolation=interpolation)


def crop_frame(frame, bbox):
    x1, y1, x2, y2 = [int(b) for b in bbox]
    cropped_frame = frame[y1:y2, x1:x2]
    return cropped_frame
