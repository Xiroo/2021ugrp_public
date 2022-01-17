from pathlib import Path
from PIL import Image, ImageFilter
import numpy as np

from dataset2 import Dataset, IterDataset
from gui2 import GUI

from ai import predict

OUTCOME_DIR = "(SET_YOUR_OWN_DIR)"
INPUT_DATA_DIR = "(SET_YOUR_OWN_DIR)"


class App(GUI):
    def __init__(self):
        super(App, self).__init__()
        self.dataset_dir = list(Path(INPUT_DATA_DIR).iterdir())
        self.outcome_dir = Path(OUTCOME_DIR)

        self.input_data = []
        for subdir in self.dataset_dir:
            self.input_data.append(Dataset(subdir))

        self.data_list = IterDataset(self.input_data)
        self.max_idx = len(self.data_list)
        self.selected = [False] * self.max_idx
        self.cur_idx = 0
        self.cur_img = None
        self.sync()

    def next_page(self):
        if self.cur_idx == self.max_idx:
            return
        self.cur_idx += 1

    def prev_page(self):
        if self.cur_idx == 0:
            return
        self.cur_idx -= 1

    def prev_button_event(self):
        try:
            self.prev_page()
        except IndexError:
            pass
        self.sync()

    def next_button_event(self):
        try:
            self.next_page()
        except IndexError:
            pass
        self.sync()

    def img_click_event(self):
        senti = predict(self.cur_img)
        self.set_senti(senti)

    def select_button_event(self):
        self.selected[self.cur_idx] = True

    def delete_button_event(self):
        self.selected[self.cur_idx] = False

    def move_button_event(self):
        inp1 = self.move_ibox1.get(1.0, "end-1c")
        self.cur_page = int(inp1)

        self.sync()

    def key_event(self, event):
        if event.char == '\r' or event.char == 'j':
            self.select_button_event()
            self.next_button_event()
        elif event.char == 'f':
            self.next_button_event()
        elif event.char == 'b':
            self.prev_button_event()
        elif event.char == 'd':
            self.delete_button_event()
            self.next_button_event()

    def img_enter_event(self):
        pass

    def img_leave_event(self):
        pass

    def sync(self):

        self.ibox1_set(str(self.cur_idx))
        img, npy = self.data_list[self.cur_idx]

        self.img_show(img)
        self.cur_img = img

        self.frm.focus_set()

    def save(self):
        cnt = 0
        for idx in range(self.max_idx):
            if self.selected[idx]:
                img, npy = self.data_list[idx]
                img.save(self.outcome_dir/f"{cnt}.jpg")
                np.save(self.outcome_dir/f"{cnt}.npy", npy)
                cnt += 1

if __name__ == "__main__":
    app = App()
    app.root.mainloop()
    app.save()
