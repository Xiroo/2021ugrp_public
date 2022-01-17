import cv2

from pathlib import Path
from PIL import Image
from skimage.metrics import structural_similarity as compare_ssim

import numpy as np


def compare_image(imageA, imageB, criteria=0.72):
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

    score, diff = compare_ssim(grayA, grayB, full=True)

    if score > criteria:
        return False
    else:
        return True


def cv2pil(img):
    color_converted = img[:, :, ::-1]
    pil_img = Image.fromarray(color_converted)
    return pil_img


def pil2cv(img):
    cv2_img = np.array(img.convert('RGB'))
    return cv2_img[:, :, ::-1].copy()


def remove_redundancy(images):
    if len(images) == 0:
        return []

    prev_img = pil2cv(images[0])
    ret = [images[0]]

    for img in images:
        cv2_img = pil2cv(img)
        if compare_image(cv2_img, prev_img):
            ret.append(img)
        if len(ret) == 25:
            return ret

    return ret
