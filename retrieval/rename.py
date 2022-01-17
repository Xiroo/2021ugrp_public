from pathlib import Path

dst = "database"

def numbering():
    p = Path(dst)
    f_list = list(p.glob('*.png'))
    for i,f in enumerate(f_list):
        fname = "%i_source.jpg"%i
        while Path(p/fname).exists == True:
            i = i+1
        f.rename(p/fname)
    print("numbering done!")

numbering()