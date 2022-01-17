from operator import truediv
from pydub import AudioSegment
from pathlib import Path
from model import predict
from db import search
from moviepy.editor import *
import os
from win32api import SetFileAttributes
from win32con import FILE_ATTRIBUTE_HIDDEN
UNIT = 1000 # 1second, Audio segment uses millisecond.


def is_windows():
    if os.name == 'nt':
        return True
    else:
        return False

def hide_file(filename):
    SetFileAttributes(filename, FILE_ATTRIBUTE_HIDDEN)

def split_by_10second(sound):
    sounds = []
    for i, chunk in enumerate(sound[::10*UNIT]):
        filename = ".processing%s.temp"%i
        with open(filename,"wb") as f:
            #if chunk is shorter than 10 second, make 10 second
            if len(chunk) != 10*UNIT: 
                makeup = AudioSegment.silent(duration = 10*UNIT - len(chunk))
                chunk = chunk.append(makeup)
            chunk.export(f, format="wav")
            sounds.append(filename)
        if is_windows() == True:
            hide_file(filename)
    return sounds

def clear_sounds(sounds):
    for file in sounds:
        if os.path.isfile(file):
            os.remove(file)

def get_duration(sound):
    return len(sound)/UNIT

def get_predicts(sounds):
    predicts = []
    for chunk in sounds:
        predicts.append(predict(chunk)[0])
    return predicts

def get_images(predicts):
    images = []
    for i in predicts:
        images.append(search(i))    
    return images

def get_imageclips(images):
    imageclips = []
    for image in images:
        imageclips.append(ImageClip(str(image)).set_duration(10))
    return imageclips

def get_audioclips(sounds):
    audioclips = []
    for audio in sounds:
        audioclips.append(AudioFileClip(str(audio)))
    return audioclips

def get_videoclips(imageclips, audioclips):
    videoclips = []
    for image, audio in zip(imageclips, audioclips):
        videoclips.append(image.set_audio(audio).set_fps(1))
    return videoclips

def close_clips(clips):
    for clip in clips:
        clip.close()

def preprocess(path):
    sound = AudioSegment.from_mp3(path)
    sounds = split_by_10second(sound)
    duration = get_duration(sound)
    predicts = get_predicts(sounds)
    images = get_images(predicts)

    return sounds, images, duration

def write_video(path):
    sounds, images, duration = preprocess(path)
    
    audioclips = get_audioclips(sounds)
    imageclips = get_imageclips(images)
    videoclips = get_videoclips(imageclips, audioclips)
    
    final_clip = concatenate_videoclips(videoclips).set_end(duration)
    final_clip.write_videofile("result.mp4")
    
    close_clips(imageclips)
    close_clips(audioclips)
    close_clips(videoclips)
    final_clip.close()
    
    clear_sounds(sounds)