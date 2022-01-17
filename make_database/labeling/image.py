import cv2
import os

from pathlib import Path
from PIL import Image
from skimage.metrics import structural_similarity as compare_ssim

if __name__ == "__main__":
    from util import create_dir, str2path
else:
    from util import create_dir, str2path


def resizeto244(img):
    size = (244, 244)
    w, h = img.size
    crop_img = img.crop(((w-h)/2, 0, (w+h)/2, h))
    resized_image = crop_img.resize(size)
    return resized_image


def cv2pil(img):
    color_converted = img[:, :, ::-1]
    pil_img = Image.fromarray(color_converted)
    return pil_img


def compare_image(imageA, imageB):
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

    score, diff = compare_ssim(grayA, grayB, full=True)

    if score > 0.72:
        return False
    else:
        return True


def capture_image(vid: cv2.VideoCapture, second):
    fps = 30
    vid.set(1, second*fps)
    ret, image = vid.read()
    return image


def video2images(video_path, image_dir):
    video_path = str2path(video_path)
    image_dir = str2path(image_dir)

    fps = 30
    unittime = 1

    vidcap = cv2.VideoCapture(str(video_path))
    vidlen = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

    create_dir(image_dir)

    second = 5
    count = 0

    while vidcap.isOpened():
        # capture video
        image = capture_image(vidcap, second)
        if image is None:
            break

        pil_img = cv2pil(image)
        resized_img = resizeto244(pil_img)

        resized_img.save(image_dir/f'{second}.jpg', "JPEG")

        second += 9
        count += 1

        if int(vidcap.get(1)) >= vidlen:
            break
    vidcap.release()
    return


if __name__ == "__main__":
    video2images("../resource/video/temp.mp4", "../for_test")
