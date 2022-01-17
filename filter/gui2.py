from tkinter import *
from tkinter import ttk

from PIL import Image, ImageTk

from pathlib import Path

SIDE = 200


class GUI:
    def __init__(self):
        self.root = Tk()

        self.root.title("Filtering Images")
        self.root.geometry("600x400")

        self.init_imgfrm()
        self.init_ui()
        self.text_ui()

        self.imgfrm.grid(row=0, column=0, columnspan=1)
        self.frm.grid(row=2, column=0, columnspan=6)
        self.text_ui_grid()
        self.ui_grid()
        self.frm.focus_set()
        self.frm.bind("<Key>", self.key_event)

    def text_ui(self):
        self.senti = ttk.Frame(self.root)
        self.pos_label = Label(self.senti, text="POS: ")
        self.nue_label = Label(self.senti, text="NUE: ")
        self.neg_label = Label(self.senti, text="NEG: ")

    def text_ui_grid(self):
        self.senti.grid(row=0, column=6)
        self.pos_label.grid(row=0, column=0)
        self.nue_label.grid(row=1, column=0)
        self.neg_label.grid(row=2, column=0)

    def ui_grid(self):
        self.move_ibox1.grid(row=1, column=1)
        self.prev_button.grid(row=1, column=0)
        self.select_button.grid(row=0, column=0)
        self.move_button.grid(row=0, column=1)
        self.delete_button.grid(row=0, column=2)
        self.next_button.grid(row=1, column=2)

    def init_imgfrm(self):
        self.imgfrm = ttk.Frame(
            self.root,
            padding=20,
            width=800,
            height=800,
            )

        self.imgbox = Label(self.imgfrm)

    def init_ui(self):
        self.frm = ttk.Frame(self.root, padding=10)

        self.move_ibox1 = Text(self.frm, height=2, width=10)
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

    def img_click_event(self):
        raise NotImplementedError

    def img_enter_event(self):
        raise NotImplementedError

    def img_leave_event(self):
        raise NotImplementedError

    def img_click_bind(self):
        def click_event_wrapper(event):
            self.img_click_event()
        return click_event_wrapper

    def img_enter_bind(self):
        def enter_event_wrapper(event):
            self.img_enter_event()
        return enter_event_wrapper

    def img_leave_bind(self):
        def leave_event_wrapper(event):
            self.img_leave_event()
        return leave_event_wrapper

    def img_hide(self):
        self.imgbox.grid_forget()
        self.imgbox.destroy()

    def img_show(self, image):
        image = image.resize((SIDE, SIDE))
        tk_image = ImageTk.PhotoImage(image)
        self.img_hide()

        img_label = Label(
            self.imgfrm,
            image=tk_image,
            width=SIDE,
            height=SIDE,
        )
        img_label.image = tk_image
        img_label.grid(row=0, column=0)
        img_label.bind(
            "<Button-1>",
            self.img_click_bind()
        )
        img_label.bind(
            "<Enter>",
            self.img_enter_bind()
        )
        img_label.bind(
            "<Leave>",
            self.img_leave_bind()
        )
        self.imgbox = img_label

    def ibox1_set(self, text):
        self.move_ibox1.delete('1.0', END)
        self.move_ibox1.insert(END, text)

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
    path = Path("../dataset/1/0.jpg")
    imgs = Image.open(path)

    app.img_show(imgs)
    app.root.mainloop()
