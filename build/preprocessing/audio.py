from pydub import AudioSegment, silence
from pathlib import Path

if __name__ == "__main__":
    from util import create_dir, str2path
else:
    from .util import create_dir, str2path


def separate(path, outcome, format='mp4', suffix='.mp4',
             min_silence_len=0.1, silence_thresh=-45, unit=1000):

    path = str2path(path)
    outcome = str2path(outcome)

    # making output directory if not exist
    create_dir(outcome)

    # get AudioSegment object from file

    if format == 'wav':
        song = AudioSegment.from_wav(path)
    else:
        song = AudioSegment.from_file(path, format=format)

    # separate audio
    chunks = silence.split_on_silence(
        song,
        min_silence_len=int(min_silence_len*unit),
        silence_thresh=silence_thresh
        )

    count = 1
    elapsed = 0
    for chunk in chunks:
        # only save when chunk length is longer than 30 second
        if len(chunk) > 30 * 1000:
            filename = f"{elapsed//1000}_{(elapsed+len(chunk))//1000}"
            fd = chunk.export((outcome/(filename+suffix)), format=format)
            fd.close()
            count += 1
        elapsed += len(chunk)

    return


def audio_cutting(path, outcome, format='mp4', suffix='.mp4'):

    path = str2path(path)
    outcome = str2path(outcome)

    # define some constant
    unit = 1000    # unit = 1s
    cut_size = 10  # result audio length = 10s
    over_lap = 1   # overlap size = 1s

    # making output directory if not exist
    create_dir(outcome)

    # extract audio
    song = AudioSegment.from_file(path, format=format)
    song_length = len(song)

    s, e = 0, 10
    i = 0
    while e*unit < song_length:
        segment = song[s*unit:e*unit]
        fd = segment.export(outcome/(f"{s}_{e}"+'.wav'), format='wav')
        fd.close()
        s += 9
        e += 9
        i += 1

    return


if __name__ == "__main__":
    audio_cutting("./temp/separated/0_274.mp4", "./dataset")
