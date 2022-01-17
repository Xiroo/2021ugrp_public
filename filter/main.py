from pathlib import Path
from PIL import Image, ImageFilter
import numpy as np

from dataset import Dataset
from gui import GUI

from image import remove_redundancy
from ai import predict

OUTCOME_DIR = "./dataset"
INPUT_DATA_DIR = "./data"


class App(GUI):
    def __init__(self):
        super(App, self).__init__()
        self.outcome = Dataset(Path(OUTCOME_DIR))
        self.dataset_dir = list(Path(INPUT_DATA_DIR).iterdir())

        self.input_data = []
        for subdir in self.dataset_dir:
            self.input_data.append(Dataset(subdir))

        self.cur_dataset_idx = 0
        self.cur_hash_idx = 0
        self.cur_dataset = self.input_data[self.cur_dataset_idx]
        self.hash_list = self.get_hash_from_cur()

        self.sync()

    def get_hash_from_cur(self):
        return self.cur_dataset.get_hash()

    def get_imgs_from_cur(self):
        cur_hash = self.hash_list[self.cur_hash_idx]
        return self.cur_dataset.get_imgs(cur_hash)

    def next_file(self):
        self.cur_hash_idx += 1
        if self.cur_hash_idx >= len(self.hash_list):
            self.cur_dataset_idx += 1
            if self.cur_dataset_idx >= len(self.input_data):
                self.cur_dataset_idx = len(self.input_data) - 1
                self.cur_hash_idx = len(self.hash_list) - 1
                raise IndexError

            self.cur_dataset = self.input_data[self.cur_dataset_idx]
            self.hash_list = self.get_hash_from_cur()
            self.cur_hash_idx = 0

    def prev_file(self):
        self.cur_hash_idx -= 1
        if self.cur_hash_idx < 0:
            self.cur_dataset_idx -= 1
            if self.cur_dataset_idx < 0:
                self.cur_hash_idx = 0
                self.cur_dataset_idx = 0
                raise IndexError

            self.cur_dataset = self.input_data[self.cur_dataset_idx]
            self.hash_list = self.get_hash_from_cur()
            self.cur_hash_idx = len(self.hash_list) - 1

    def prev_button_event(self):
        try:
            self.prev_file()
        except IndexError:
            pass
        self.sync()

    def next_button_event(self):
        try:
            self.next_file()
        except IndexError:
            pass
        self.sync()

    def select_button_event(self):
        hash = self.hash_list[self.cur_hash_idx]
        data = self.cur_dataset.get_pairs(hash)
        title = self.cur_dataset.get_title(hash)
        self.outcome.append(hash, data, title)

    def delete_button_event(self):
        hash = self.hash_list[self.cur_hash_idx]
        self.outcome.delete(hash)

    def move_button_event(self):
        inp1 = self.move_ibox1.get(1.0, "end-1c")
        inp2 = self.move_ibox2.get(1.0, "end-1c")
        self.cur_dataset_idx = int(inp1)
        self.cur_hash_idx = int(inp2)

        self.sync()

    def key_event(self, event):
        if event.char == '\r':
            self.select_button_event()
            self.next_button_event()
        elif event.char == 'f':
            self.next_button_event()
        elif event.char == 'b':
            self.prev_button_event()
        elif event.char == 'd':
            self.delete_button_event()
            self.next_button_event()

    def img_enter_event(self, i, j):
        pass

    def img_leave_event(self, i, j):
        pass

    def img_click_event(self, i, j):
        idx = i * 5 + j
        senti = predict(self.cur_img[idx])
        self.set_senti(senti)

    def sync(self):
        hash = self.hash_list[self.cur_hash_idx]

        self.ibox1_set(str(self.cur_dataset_idx))
        self.ibox2_set(str(self.cur_hash_idx))

        self.set_title(self.cur_dataset.get_title(hash))

        images = self.get_imgs_from_cur()
        images = remove_redundancy(images)
        self.img_show(images)
        self.cur_img = images

        self.frm.focus_set()


if __name__ == "__main__":
    app = App()
    app.root.mainloop()
