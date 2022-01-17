import csv

VID_TITTLE = 0
YT_PATH = 1
THUMB_PATH = 2
CHANNEL = 3


def to_second(time):
    time = time.split(':')
    time = list(map(int, time))
    second = 0
    if len(time) == 2:
        second += time[0] * 60
        second += time[1]
    elif len(time) == 3:
        second += time[0] * 3600
        second += time[1] * 60
        second += time[2]
    return second
