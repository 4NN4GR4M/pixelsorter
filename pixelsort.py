import numpy as np
import cv2 as cv
from sympy import *


def return_max_val_idx(img, col_idx):
    highest_sum_idx = 0
    highest_sum = 0
    for i in range(img.shape[0]):
        if img[i, col_idx].sum() > highest_sum and not (i < img.shape[0]*0.1) and not (i > img.shape[0]*0.6):
            highest_sum = img[i, col_idx].sum()
            highest_sum_idx = i
            
    return highest_sum_idx


def pixelsorter(filepath_in, filepath_out, vertical_sort_restraint=1, activate_filter=True, thread_height_reduction=1, thread_width=1, noise_intensity=100):
    img = cv.imread(filepath_in, -1)

    if activate_filter:
        noise = np.zeros(img.shape, np.uint8)
        mean = 0
        deviation = noise_intensity
        cv.randn(noise, mean, deviation)

        img = cv.add(img, noise)

    print(img.shape)
    IMG_HEIGHT = int(img.shape[0] * thread_height_reduction)
    
    for col in range(img.shape[1]):
        thread_start_idx = return_max_val_idx(img, col)

        if IMG_HEIGHT > thread_start_idx*2: row_range = [thread_start_idx, IMG_HEIGHT - thread_start_idx]
        else: row_range = [thread_start_idx, IMG_HEIGHT]

        if col % vertical_sort_restraint == 0:
            img[row_range[0]:row_range[1], col:col+thread_width] = -np.partition(-img[row_range[0]:row_range[1], col:col+thread_width], axis=0, kth=int((row_range[1]-row_range[0])/4))

    cv.imwrite(filepath_out, img)
