import importlib
import sys

import numpy as np
import torch
import torchvision.transforms as t
from torchvision.datasets.folder import default_loader

from PIL import Image
from pathlib import Path

cur_dir = Path(Path(__file__).parent)
vsa_dir = cur_dir/"visual-sentiment-analysis"
tmp_dir = cur_dir / "tmp"

model_dir = "converted-models"
model_pth = "vgg19_finetuned_all.pth"

if not tmp_dir.exists():
    tmp_dir.mkdir()

sys.path.append(str(vsa_dir))

vgg19 = importlib.import_module("vgg19")
model = vgg19.KitModel(vsa_dir/model_dir/model_pth).to('cuda')
model.eval()


def tmp_func(x):
    return x[[2, 1, 0], ...] * 255


transform = t.Compose(
    [
        t.Resize((224, 224)),
        t.ToTensor(),
        t.Lambda(tmp_func),
        t.Normalize(mean=[116.8007, 121.2751, 130.4602], std=[1, 1, 1]),
    ]
)


def predict(image):
    with torch.no_grad():
        x = transform(image)
        x = torch.unsqueeze(x, 0)
        p = model(x.to('cuda')).cpu()
        return p.numpy()[0]


if __name__ == "__main__":
    img = Image.open("./data/data1/0.jpg")
    print(predict(img))
