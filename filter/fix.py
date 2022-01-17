from pathlib import Path
import csv
import os
import argparse

if __name__ != "__main__":
    raise ImportError("This module cannot be imported")

def dir_path(string):
    if  os.path.exists(string):
        if os.path.isdir(string):
            return string
        else:
            raise NotADirectoryError(string)
    else:
        raise FileNotFoundError(string)

parser = argparse.ArgumentParser(description="Fix the dataset to remove fragmentation")
parser.add_argument('path', type=dir_path)

args = parser.parse_args()

DATASET_DIR = args.path

DATASET_DIR = Path(DATASET_DIR)

result = []

with open(DATASET_DIR / "data.csv", newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        result.append(row)

count = 0
for row in result:
    hash = row[0]
    s = int(row[1])
    e = int(row[2])
    prev_count = count

    for i in range(s, e):
        img_name = DATASET_DIR / f"{i}.jpg"
        npy_name = DATASET_DIR / f"{i}.npy"
        new_img_name = DATASET_DIR / f"{count}.jpg"
        new_npy_name = DATASET_DIR / f"{count}.npy"

        img_name.rename(new_img_name)
        npy_name.rename(new_npy_name)
        count += 1

    row[1] = prev_count
    row[2] = count

with open(DATASET_DIR / "result.csv", newline='', mode='w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for row in result:
        writer.writerow(row)

(DATASET_DIR/"result.csv").rename(DATASET_DIR/"data.csv")