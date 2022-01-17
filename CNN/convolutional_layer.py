import torch
from torch import nn
from torch.nn import Conv2d, ReLU, BatchNorm2d, MaxPool2d


class AudioCNN(nn.Module):
    def __init__(self):
        super(AudioCNN, self).__init__()

        self.layer1 = nn.Sequential(
            Conv2d(in_channels=1, out_channels=64, kernel_size=3, padding=1),
            BatchNorm2d(64),
            ReLU(),
            Conv2d(in_channels=64, out_channels=64, kernel_size=3, padding=1),
            BatchNorm2d(64),
            ReLU(),
            MaxPool2d(kernel_size=2, stride=2)
        )

        self.layer2 = nn.Sequential(
            Conv2d(in_channels=64, out_channels=128, kernel_size=3, padding=1),
            BatchNorm2d(128),
            ReLU(),
            Conv2d(in_channels=128, out_channels=128,
                   kernel_size=3, padding=1),
            BatchNorm2d(128),
            ReLU(),
            MaxPool2d(kernel_size=2, stride=2)
        )

        self.layer3 = nn.Sequential(
            Conv2d(in_channels=128, out_channels=256,
                   kernel_size=3, padding=1),
            BatchNorm2d(256),
            ReLU(),
            Conv2d(in_channels=256, out_channels=256,
                   kernel_size=3, padding=1),
            BatchNorm2d(256),
            ReLU(),
            MaxPool2d(kernel_size=2, stride=2)
        )

        self.layer4 = nn.Sequential(
            Conv2d(in_channels=256, out_channels=512,
                   kernel_size=3, padding=1),
            BatchNorm2d(512),
            ReLU(),
            Conv2d(in_channels=512, out_channels=512,
                   kernel_size=3, padding=1),
            BatchNorm2d(512),
            ReLU(),
            MaxPool2d((32, 24)),
        )

        self.fc1 = nn.Linear(512, 128)
        self.fc2 = nn.Linear(128, 3)

        self.flatten = nn.Flatten()
        self.ReLU = ReLU()
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)

        x = self.flatten(x)
        x = self.fc1(x)
        x = self.ReLU(x)
        x = self.fc2(x)
        return x


if __name__ == "__main__":
    t = torch.zeros([1, 1, 257, 199], dtype=torch.double)
    t = t.float()
    a = AudioCNN()
    print(a(t))
