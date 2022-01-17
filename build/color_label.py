import os
import argparse
import numpy as np
from pathlib import Path
import cv2 as cv
import numpy as np
from collections import Counter

from sklearn.cluster import KMeans


def dir_path(string):
    if os.path.exists(string):
        if os.path.isdir(string):
            return string
        else:
            raise NotADirectoryError(string)
    else:
        raise FileNotFoundError(string)


parser = argparse.ArgumentParser(
    description="Make label.csv for given dataset"
    )
parser.add_argument('path', type=dir_path)

args = parser.parse_args()

path = Path(args.path)

outcome = list(path.glob("*.jpg"))
predict_result = [None] * len(outcome)


def predict(color, perc):
    pass


for file in outcome:
    idx = int(file.stem)
    npy_filename = file.with_suffix(".npy")
    img = cv.imread(str(file))

    clt = KMeans(n_clusters=5)

    clt.fit(img.reshape(-1, 3))
    cluster = clt.cluster_centers_
    n_pixels = len(clt.labels_)
    rank = Counter(clt.labels_).most_common(5)

    perc = []
    main_color = []

    for color, n_color_pixel in rank:
        perc.append(np.round(n_color_pixel/n_pixels, 2))
        main_color.append(cluster[color])

    predict_result[idx] = predict(main_color, perc)
