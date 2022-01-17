import pytube
import urllib.request
from pathlib import Path

from .variable import VID_PATH


def getVideo(streams, outcome, filename=None):
    video_dir = outcome
    streams.download(
        output_path=video_dir,
        filename=filename
        )


def getAudio(streams, outcome, filename=None):
    audio_dir = outcome
    streams.download(
        output_path=audio_dir,
        filename=filename
    )


def get_from_yt(vidId, vidpath: Path, audpath: Path):
    yt = pytube.YouTube(VID_PATH.format(vidId))

    try:
        vid_stream = yt.streams.filter(
            progressive=True,
            file_extension='mp4'
            )[0]

        getVideo(vid_stream, str(vidpath.parent), vidpath.name)

        aud_stream = yt.streams.filter(
            only_audio=True,
            file_extension='mp4'
            )[0]

        getAudio(aud_stream, str(audpath.parent), audpath.name)

    except(pytube.exceptions.LiveStreamError):
        print('[!] This is live streaming video')
