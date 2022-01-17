import torch
from torch import nn
import librosa
import numpy as np
from numpy import max
import convolutional_layer as mycnn


def MFCC(audio_path):
    wav_path = audio_path

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

    return mfcc

device = "cuda"

model = mycnn.AudioCNN()
model = model.to(device)


def load():
    model.load_state_dict(torch.load('model_weights.pth'))


load()


def predict(audio_path):
    mfcc = torch.Tensor(MFCC(audio_path))
    mfcc = np.expand_dims(mfcc, axis = (0,1))
    model.eval()
    with torch.no_grad():
        mfcc = torch.Tensor(mfcc).to(device)
        pred = model(mfcc)
    return model.softmax(pred).tolist()
