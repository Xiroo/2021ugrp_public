from tkinter import *
from tkinter import ttk

from PIL import Image, ImageTk

from pathlib import Path

SIDE = 140


class GUI:
    def __init__(self):
        self.root = Tk()

        self.root.title("Filtering Images")
        self.root.geometry("900x900")

        self.init_imgfrm()
        self.init_ui()
        self.text_ui()

        self.imgfrm.grid(row=0, column=0, columnspan=5)
        self.frm.grid(row=2, column=0, columnspan=6)
        self.text_ui_grid()
        self.ui_grid()
        self.frm.focus_set()
        self.frm.bind("<Key>", self.key_event)

    def text_ui(self):
        self.vid_title = Label(self.root, text="This is title", width=80)

        self.senti = ttk.Frame(self.root)
        self.pos_label = Label(self.senti, text="POS: ")
        self.nue_label = Label(self.senti, text="NUE: ")
        self.neg_label = Label(self.senti, text="NEG: ")

    def text_ui_grid(self):
        self.vid_title.grid(row=1, column=0, columnspan=5)
        self.senti.grid(row=0, column=6)
        self.pos_label.grid(row=0, column=0)
        self.nue_label.grid(row=1, column=0)
        self.neg_label.grid(row=2, column=0)

    def ui_grid(self):
        self.move_ibox1.grid(row=0, column=2)
        self.move_ibox2.grid(row=0, column=4)
        self.prev_button.grid(row=1, column=0)
        Label(self.frm, text="", width=3).grid(row=1, column=1)
        self.select_button.grid(row=1, column=2)
        self.move_button.grid(row=1, column=3)
        self.delete_button.grid(row=1, column=4)
        Label(self.frm, text="", width=3).grid(row=1, column=5)
        self.next_button.grid(row=1, column=6)

    def init_imgfrm(self):
        self.imgfrm = ttk.Frame(
            self.root,
            padding=20,
            width=800,
            height=800,
            )

        self.imgbox = []
        self.img_fill_empty(0)

    def init_ui(self):
        self.frm = ttk.Frame(self.root, padding=10)

        self.move_ibox1 = Text(self.frm, height=2, width=10)
        self.move_ibox2 = Text(self.frm, height=2, width=10)
        self.move_button = ttk.Button(
            self.frm,
            command=self.move_button_event,
            text="Move",
            width=10
            )

        self.prev_button = ttk.Button(
            self.frm,
            command=self.prev_button_event,
            width=10,
            text="Prev",
        )
        self.select_button = ttk.Button(
            self.frm,
            command=self.select_button_event,
            width=10,
            text="Select",
        )
        self.delete_button = ttk.Button(
            self.frm,
            command=self.delete_button_event,
            width=10,
            text="Delete",
        )
        self.next_button = ttk.Button(
            self.frm,
            command=self.next_button_event,
            width=10,
            text="Next",
        )

    def prev_button_event(self):
        raise NotImplementedError

    def next_button_event(self):
        raise NotImplementedError

    def select_button_event(self):
        raise NotImplementedError

    def delete_button_event(self):
        raise NotImplementedError

    def move_button_event(self):
        raise NotImplementedError

    def key_event(self, event):
        raise NotImplementedError

    def img_click_event(self, i, j):
        raise NotImplementedError

    def img_enter_event(self, i, j):
        raise NotImplementedError

    def img_leave_event(self, i, j):
        raise NotImplementedError

    def img_click_bind(self, i, j):
        def click_event_wrapper(event):
            self.img_click_event(i, j)
        return click_event_wrapper

    def img_enter_bind(self, i, j):
        def enter_event_wrapper(event):
            self.img_enter_event(i, j)
        return enter_event_wrapper

    def img_leave_bind(self, i, j):
        def leave_event_wrapper(event):
            self.img_leave_event(i, j)
        return leave_event_wrapper

    def img_fill_empty(self, idx):
        empty_img = ImageTk.PhotoImage(
            Image.open("empty.jpg").resize((SIDE, SIDE))
        )

        while idx < 25:
            img_label = Label(
                self.imgfrm,
                width=SIDE,
                height=SIDE,
                image=empty_img
            )
            img_label.grid(
                row=idx//5,
                column=idx % 5,
            )
            self.imgbox.append(img_label)
            idx += 1

    def img_hide(self):
        for label in self.imgbox:
            label.grid_forget()
            label.destroy()

    def img_show(self, images):
        images = [img.resize((SIDE, SIDE)) for img in images]
        tk_imgs = [ImageTk.PhotoImage(img) for img in images]

        idx = -1
        self.img_hide()
        self.imgbox = []
        for idx, img in enumerate(tk_imgs):
            if idx >= 25:
                break
            img_label = Label(
                self.imgfrm,
                image=img,
                width=SIDE,
                height=SIDE,
                )
            img_label.image = img
            img_label.grid(
                row=idx//5,
                column=idx % 5,
            )
            img_label.bind(
                "<Button-1>",
                self.img_click_bind(idx//5, idx % 5)
            )
            img_label.bind(
                "<Enter>",
                self.img_enter_bind(idx//5, idx % 5)
            )
            img_label.bind(
                "<Leave>",
                self.img_leave_bind(idx//5, idx % 5)
            )
            self.imgbox.append(img_label)
        self.img_fill_empty(idx+1)

    def ibox1_set(self, text):
        self.move_ibox1.delete('1.0', END)
        self.move_ibox1.insert(END, text)

    def ibox2_set(self, text):
        self.move_ibox2.delete('1.0', END)
        self.move_ibox2.insert(END, text)

    def set_title(self, text):
        self.vid_title.configure(text=text)

    def set_senti(self, senti):
        pos = senti[2]
        neu = senti[1]
        neg = senti[0]

        self.pos_label.configure(text=f"POS: {pos:>3f}")
        self.nue_label.configure(text=f"NEU: {neu:>3f}")
        self.neg_label.configure(text=f"NEG: {neg:>3f}")

        ls = [(neg, 0), (neu, 1), (pos, 2)]
        ls.sort(reverse=True)

        self.set_senti_color(ls[0][1], "red")
        self.set_senti_color(ls[1][1], "black")
        self.set_senti_color(ls[2][1], "blue")

    def set_senti_color(self, idx, color):
        if idx == 0:
            self.neg_label.configure(fg=color)
        elif idx == 1:
            self.nue_label.configure(fg=color)
        elif idx == 2:
            self.pos_label.configure(fg=color)


if __name__ == "__main__":
    app = GUI()
    path_list = list(Path("./data/data1").glob("*.jpg"))
    imgs = [
        Image.open(path) for path in path_list[0:10]
        ]

    app.img_show(imgs)
    app.root.mainloop()
