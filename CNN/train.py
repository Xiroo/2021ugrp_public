import torch
from torch import nn
from torch.nn.modules import loss
import convolutional_layer as mycnn
from DataLoader import train_loader, test_loader

import atexit

learning_rate = 1e-3
weight_decay = 1e-5
epochs = 30

device = "cuda"

model = mycnn.AudioCNN().to(device)

loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(
    model.parameters(),
    lr=learning_rate,
    weight_decay=weight_decay,
    )


def train(dataloader, model, loss_fn, optimizer):
    size = len(dataloader.dataset)
    model.train()
    for batch, (X, y) in enumerate(dataloader):
        X, y = X.to(device), y.to(device)
        pred = model(X)
        loss = loss_fn(pred, y)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if batch % 100 == 0:
            loss, current = loss.item(), batch * len(X)
            print(f"loss: {loss:>7f} [{current:>5d}/{size:>5d}]")


def test(dataloader, model, loss_fn):
    size = len(dataloader.dataset)
    num_batches = len(dataloader)
    model.eval()
    test_loss, correct = 0, 0
    with torch.no_grad():
        for X, y in dataloader:
            X, y = X.to(device), y.to(device)
            pred = model(X)
            test_loss += loss_fn(pred, y).item()
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()
    test_loss /= num_batches
    correct /= size

    print("Test Error: ")
    print(f" Accuracy: {(100*correct):>0.1f}%")
    print(f" Avg loss: {test_loss:>8f}")


def save():
    torch.save(model.state_dict(), 'model_weights.pth')


def load():
    model.load_state_dict(torch.load('model_weights.pth'))


if __name__ == "__main__":
    for count in range(epochs):
        print(f"[+] Epoch {count}\n----------------------")
        train(train_loader, model, loss_fn, optimizer)
        test(test_loader, model, loss_fn)
    save()
    print("[+] Training completed")
    test(train_loader, model, loss_fn)
    print("[+] Test complete")
