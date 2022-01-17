from pathlib import Path
import csv


def log(msg):
    with open("./log.txt", "a") as f:
        f.write(msg)


def record_meta(vid, s, e):
    with open(
        "./data.csv",
        "a",
        newline='',
        encoding='UTF-8'
    ) as csvfile:
        writer = csv.writer(csvfile)
        row = [vid, s, e]
        writer.writerow(row)


def job_logger(job):
    def decorator(func):
        def decorated(*args, **kwargs):
            log(job)
            func(*args, **kwargs)
            log("  complete\n")
        return decorated
    return decorator
