import matplotlib.pyplot as plt
import librosa.display
import librosa
from pydub import AudioSegment

import numpy as np

from numpy import max, save
from pathlib import Path


def mpeg2wav(video: Path):
    song = AudioSegment.from_file(video, format="mp4")
    song.export(str(video.with_suffix('.wav')), format="wav")
    return video.with_suffix('.wav')


def MFCC(videopath: Path, outcome: Path):
    wav_path = videopath

    x, sr = librosa.load(wav_path)
    S = librosa.feature.melspectrogram(
        x,
        sr=sr,
        n_mels=257,
        hop_length=int(0.05*sr),
        n_fft=int(0.1*sr),
        )

    # S.shape = (257, 201)
    S = S[:, :199]

    log_S = librosa.power_to_db(S, ref=max)
    mfcc = librosa.feature.mfcc(S=log_S, n_mfcc=257)
    delta2_mfcc = librosa.feature.delta(mfcc, order=1)

    result = np.array([log_S, mfcc, delta2_mfcc])
    save(outcome, result)

    return result


def show(mfcc_result):
    plt.figure(figsize=(12, 4))
    librosa.display.specshow(mfcc_result)
    plt.ylabel('MFCC coeffs')
    plt.xlabel('Time')
    plt.title('MFCC')
    plt.colorbar()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    mfcc = MFCC(Path('./temp/cutted_audio/9_19.wav'), Path('./0.npy'))
    show(mfcc[0])
