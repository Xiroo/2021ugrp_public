from pathlib import Path
from PIL import Image, ImageFile
import csv

SUFFIX = "png"
ImageFile.LOAD_TRUNCATED_IMAGES = True

def resizeto244(img):
    size = (1920, 1080)
    w, h = img.size
    crop_img = img.crop(((w-h)/2, 0, (w+h)/2, h))
    resized_image = crop_img.resize(size)
    return resized_image

def resize_png():
    outcome = list(Path("database").glob(f"*.{SUFFIX}"))
    datasetdir = Path("database")
    for idx in range(len(outcome)):
        img = Image.open(datasetdir/f"{idx}_source.{SUFFIX}")
        resized_img = resizeto244(img)
        resized_img = resized_img.convert("RGB")
        resized_img.save(datasetdir/f'{idx}.jpg', "JPEG")
        img.close()
        resized_img.close()
        print(f"[+] Convert completed {idx}-th image")
    print("convert to jpg done!")

def clear_png():
    p = list(Path("database").glob(f"*_source.{SUFFIX}"))
    for idx, f in enumerate(p):
        f.unlink()
        print(f"[+] clear completed {idx}-th image")
    print("clear done!")

resize_png()
clear_png()
