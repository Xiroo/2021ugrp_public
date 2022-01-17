from ctypes import resize
import os
import argparse

from ai import predict
from dataset import Dataset
from pathlib import Path
from PIL import Image, ImageFile
import csv
from image import resizeto244

SUFFIX = "png"
ImageFile.LOAD_TRUNCATED_IMAGES = True


def dir_path(string):
    if  os.path.exists(string):
        if os.path.isdir(string):
            return string
        else:
            raise NotADirectoryError(string)
    else:
        raise FileNotFoundError(string)

parser = argparse.ArgumentParser(description="Make label.csv for given dataset")
parser.add_argument('path', type=dir_path)

args = parser.parse_args()


predict_result = []
outcome = list(Path(args.path).glob(f"*.{SUFFIX}"))
datasetdir = Path(args.path)
for idx in range(len(outcome)):
    img = Image.open(datasetdir/f"{idx}_source.{SUFFIX}")
    resized_img = resizeto244(img)
    resized_img = resized_img.convert("RGB")
    resized_img.save(datasetdir/f'{idx}.jpg', "JPEG")
    img.close()
    resized_img.close()
    print(f"[+] Convert completed {idx}-th image")
print("convert to jpg done!")

for idx in range(len(outcome)):
    img = Image.open(datasetdir/f"{idx}.jpg")
    pred = predict(img)
    filename = f"{idx}.npy"

    predict_result.append([filename, pred])
    img.close()

    if idx % 1000 == 0:
        print(f"[+] Completed {idx}-th image")

with open("./label.csv", newline='', mode='w') as csvfile:
    writer = csv.writer(csvfile)
    for row in predict_result:
        writer.writerow(row)
print("labeling done!")

jpgs = list(Path(args.path).glob("*.jpg"))

for f in jpgs:
    f.unlink()
    print(f"[+] cleard {f}")
print("clear done!")
