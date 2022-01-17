from pathlib import Path
import csv
from PIL import Image
import numpy as np


class Dataset:
    def __init__(self, dataset_dir: Path):
        self.dir = dataset_dir
        self.csv_name = dataset_dir / "data.csv"

        self.csv_name.touch(exist_ok=True)

        self.img_list = list(dataset_dir.glob("*.jpg"))
        self.img_list.sort()

        self.metadata = self.parse_csv()

        max = 0
        for row in self.metadata:
            if int(row[2]) > max:
                max = int(row[2])
        self.length = max

    def parse_csv(self):
        result = []
        with open(self.csv_name, newline='', encoding='UTF8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                result.append(row)
        return result

    def get_hash(self):
        hash = []
        with open(self.csv_name, newline='', encoding='UTF8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                hash.append(row[0])
        return hash

    def get_imgs(self, hash):
        """
            Get images from dataset by hash value
            CAUTION! : should close images after using list
        """
        file_list = self.get_img_names(hash)
        images = []
        for filename in file_list:
            img = Image.open(filename)
            images.append(img)
        return images

    def get_pairs(self, hash):
        s, e = self.get_interval(hash)
        result = []
        for i in range(s, e):
            img = Image.open(self.dir/f"{i}.jpg")
            npy = np.load(self.dir / f"{i}.npy")
            result.append((img, npy))
        return result

    def get_img_names(self, hash):
        """
            Get image names from dataset by hash value
        """
        s, e = self.get_interval(hash)
        return [self.dir/f"{i}.jpg" for i in range(s, e)]

    def get_interval(self, hash):
        """
            Find interval corresponding with hash value.
            Returned interval means the set of image, npy file name stem.
        """
        s = None
        for row in self.metadata:
            if row[0] == hash:
                s = row[1]
                e = row[2]
                break

        if s is None:
            raise Exception("Hash value not found")
        return (int(s), int(e))

    def get_title(self, hash):
        for row in self.metadata:
            if row[0] == hash:
                return row[3]
        raise Exception("Hash value not found")

    def __getitem__(self, idx):
        if idx >= self.length or idx < 0:
            raise IndexError
        img = Image.open(self.dir / f"{idx}.jpg")
        npy = np.load(self.dir / f"{idx}.npy")
        return (img, npy)

    def append(self, hash, data, title, close=True):
        found = False
        for idx, row in enumerate(self.metadata):
            if row[0] == hash:
                found = True
                break
        if found:
            return

        s = self.length

        for (img, npy) in data:
            img.save(self.dir / f"{self.length}.jpg")
            np.save(self.dir / f"{self.length}.npy", npy)

            if close:
                img.close()
            self.length += 1

        e = self.length

        with open(
            self.csv_name,
            newline='',
            mode='a',
            encoding='UTF8'
        ) as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([hash, s, e, title])
            self.metadata.append([hash, s, e, title])

    def delete(self, hash):
        found = False
        for idx, row in enumerate(self.metadata):
            if row[0] == hash:
                s = int(row[1])
                e = int(row[2])
                found = True
                break

        if not found:
            raise Exception("Hash not found")
        del self.metadata[idx]

        for idx in range(s, e):
            (self.dir/f"{idx}.jpg").unlink()
            (self.dir/f"{idx}.npy").unlink()

        # modify csv file & metadata
        with open(
            self.dir/"temp.csv",
            newline='',
            mode='w',
            encoding='UTF8'
        ) as csvfile:
            writer = csv.writer(csvfile)
            for row in self.metadata:
                writer.writerow(row)

        # change filename from temp.csv to data.csv
        self.csv_name.unlink()
        (self.dir/"temp.csv").rename(self.csv_name)

    def __len__(self):
        return self.length


class IterDataset:
    def __init__(self, list_dataset):
        self.list_dataset = list_dataset
    
    def __getitem__(self, idx):
        for (tmp, dset) in enumerate(self.list_dataset):
            if idx < len(dset):
                break
            idx -= len(dset)
        if idx > len(self.list_dataset[-1]):
            raise IndexError
        return self.list_dataset[tmp][idx]

    def __len__(self):
        ret = 0
        for dset in self.list_dataset:
            ret += len(dset)
        return ret