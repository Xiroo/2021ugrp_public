from shutil import copy2
from pathlib import Path


src_dir = "images"
dst = "database"

def copy():
    p = Path(src_dir)
    f_list = list(p.glob('*/*.png'))
    for f in f_list:
        src = f
        copy2(src, dst)
    print("copy done!")

def numbering():
    p = Path(dst)
    f_list = list(p.glob('*.png'))
    for i,f in enumerate(f_list):
        fname = "%i_source.png"%i
        while Path(p/fname).exists == True:
            i = i+1
        f.rename(p/fname)
    print("numbering done!")

copy()
numbering()