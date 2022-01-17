from torch.utils.data import Dataset, DataLoader
from pathlib import Path
from torch import is_tensor
from numpy import load, expand_dims
import numpy as np

from path import *

import csv

SUFFIX = ".npy"  # change suffix to use another format.

DATA_PATH_TRAINING = list(DATASET_DIR.glob('*'+SUFFIX))
DATA_PATH_TESTING = list(DATASET_DIR.glob('*'+SUFFIX))

LABEL_PATH = DATASET_DIR / "label.csv"


class CustomDataset(Dataset):
    def __init__(self, data_path, label_file: Path, transform=None):
        self.path = data_path
        self.label = []
        with open(label_file) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                row[1] = row[1].lstrip('[').rstrip(']').split()
                row[1] = list(map(float, row[1]))
                self.label.append(np.argmax(row[1]))
        self.transform = transform

    def __len__(self):
        return len(self.path)

    def __getitem__(self, idx):
        raise NotImplementedError


class Log_S_Dataset(CustomDataset):
    def __getitem__(self, idx):
        if is_tensor(idx):
            idx = idx.tolist()

        data = load(self.path[idx])[0]
        if self.transform is not None:
            data = self.transform(data)
        data = expand_dims(data, 0)

        return data, np.array(self.label[idx])


class MFCC_Dataset(CustomDataset):
    def __getitem__(self, idx):
        if is_tensor(idx):
            idx = idx.tolist()

        data = load(self.path[idx])[1]
        if self.transform is not None:
            data = self.transform(data)
        data = expand_dims(data, 0)

        return data, np.array(self.label[idx])


class Delta_MFCC_Dataset(CustomDataset):
    def __getitem__(self, idx):
        if is_tensor(idx):
            idx = idx.tolist()

        data = load(self.path[idx])[2]
        if self.transform is not None:
            data = self.transform(data)
        data = expand_dims(data, 0)

        return data, np.array(self.label[idx][1])


train_loader = DataLoader(
    MFCC_Dataset(DATA_PATH_TRAINING, Path("./label.csv")),
    shuffle=True,
    batch_size=64,
    num_workers=4,
    persistent_workers=True,
)

test_loader = DataLoader(
    MFCC_Dataset(DATA_PATH_TRAINING, Path("./label.csv")),
    shuffle=True,
    batch_size=64,
    num_workers=4,
    persistent_workers=True,
)
"""
logs_train_loader = DataLoader(
    Log_S_Dataset(),
    shuffle=True,
    batch_size=64,
)

logs_test_loader = DataLoader(
    Log_S_Dataset(),
    shuffle=True,
    batch_size=64,
)
"""
if __name__ == "__main__":
    dataset = MFCC_Dataset(DATA_PATH_TRAINING, LABEL_PATH)
    dataset2 = Delta_MFCC_Dataset(DATA_PATH_TRAINING, LABEL_PATH)

    print(dataset[0])
    print(dataset2[0])
