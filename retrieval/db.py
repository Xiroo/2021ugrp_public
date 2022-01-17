from pathlib import Path
from PIL import Image

import csv

LABEL_FILE = Path("./database/label.csv")
IMAGE_DIR = Path("./database")
DIST_MAX = 3

result = {}

with open(LABEL_FILE) as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        filename = row[0]
        row[1] = row[1].lstrip('[').rstrip(']').split()
        label = list(map(float, row[1]))
        result[filename] = label


def dist(a, b):
    x = a[0] - b[0]
    y = a[1] - b[1]
    z = a[2] - b[2]
    return x * x + y * y + z * z


def search(label):
    min = DIST_MAX
    ret_file = None

    for filename in result:
        d = dist(result[filename], label)
        if d < min:
            min = d
            ret_file = filename
            ret_file = Path(ret_file).stem+".jpg"

    return IMAGE_DIR/ret_file