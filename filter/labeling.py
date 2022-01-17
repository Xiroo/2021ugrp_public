import os
import argparse

from ai import predict
from dataset import Dataset
from pathlib import Path
from PIL import Image
import csv


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
outcome = list(Path(args.path).glob("*.jpg"))
datasetdir = Path(args.path)

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
