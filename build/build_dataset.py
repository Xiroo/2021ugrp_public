from shutil import copyfile
from pathlib import Path
import numpy as np
import csv

import preprocessing as pp
import crawling as crl
import clean

from discords import post_message, post_err
import log


vid_file = Path("./temp/video.mp4")
aud_file = Path("./temp/audio.mp4")

temp_image_dir = Path("./temp/captured_image")
temp_separated = Path('./temp/separated')
temp_audio_cutted = Path("./temp/cutted_audio")

dataset_dir = Path("./dataset")


@log.job_logger("\tseparate")
def separate(*args, **kwargs):
    pp.separate(*args, **kwargs)


@log.job_logger("\timage capture")
def video2images(*args, **kwargs):
    pp.video2images(*args, **kwargs)


@log.job_logger("\taudio cutting")
def audio_cutting(*args, **kwargs):
    pp.audio_cutting(*args, **kwargs)


def get_ids_from_file(filename):
    ids = []
    with open(filename, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            ids.append(line.rstrip())
    return ids


def load_from_data():
    with open("./data.csv") as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)
        if len(rows) == 0:
            return None, 0
        row = rows[-1]
    last_id = row[0]
    last_file = int(row[2])
    return last_id, last_file


if __name__ == "__main__":
    ids = get_ids_from_file("./id_list.txt")

    last_id, count = load_from_data()
    prev_count = count
    idx = 0

    if last_id is not None:
        idx = ids.index(last_id) + 1
        ids = ids[idx:]

    pp.create_dir(Path("./temp"))
    try:
        for id in ids:
            # init log
            log.log(f"{idx}th video\n")
            log.log(f"\tid: {id}\n")

            # download the video
            try:
                crl.get_from_yt(id, vid_file, aud_file)
            except(Exception):
                log.record_meta(id, prev_count, count)
                continue

            log.log("\tDownload complete\n")

            # separation
            separate(
                aud_file,
                temp_separated,
                )

            # image capture
            video2images(
                vid_file,
                temp_image_dir
            )

            # get captured image list
            image_list = list(temp_image_dir.glob('*'))

            # parse the list to get a second information
            image_secs = [img.stem for img in image_list]

            # get song list from "separated" directory
            songs = list(temp_separated.glob('*'))

            for (i, song) in enumerate(songs):

                # file name of separated song file is (start_time)_(end_time)
                s, e = song.stem.split('_')

                # image file stem correspond with song
                song_img = [sec for sec in image_secs if s <= sec and sec < e]
                song_img.sort()

                # trim song file to 10 secs audio segment
                audio_cutting(
                    song,
                    temp_audio_cutted,
                    )

                # get 10 secs audio chunk list
                # chunk file format = wav
                chunks = list(temp_audio_cutted.glob('*'))
                for chunk in chunks:

                    # get time information about chunk
                    seg_s, seg_e = chunk.stem.split('_')
                    seg_s += s
                    seg_e += s

                    sec = None
                    # find image correspond with song by time information
                    for (i, sec) in enumerate(song_img):
                        if seg_s <= sec and sec < seg_e:
                            break

                    # no image, then just remove the audio chunk
                    if sec is None or seg_s > sec or sec >= seg_e:
                        chunk.unlink()
                        continue

                    # move the image to dataset
                    img_filename = temp_image_dir/f"{sec}.jpg"
                    copyfile(str(img_filename), str(dataset_dir/f"{count}.jpg"))

                    # convert the audio to mfcc and save
                    pp.MFCC(chunk, dataset_dir/f"{count}.npy")

                    chunk.unlink()

                    count += 1

                # remove file
                song.unlink()

            log.record_meta(id, prev_count, count)
            prev_count = count

            # completion log
            log.log(f"Complted {idx}th video\n")
            post_message(f"video {id} Complete")

            # clean up temp file
            clean.cleanup()
            vid_file.unlink()
            aud_file.unlink()
            idx += 1
    except Exception as e:
        post_err(e)
        log.log(e)
