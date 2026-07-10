from torchvision import transforms
from datasets import load_dataset
from genaibook.core import show_images
import matplotlib as mpl
# import matplotlib.pyplot as plt
from torch.utils.data import DataLoader
from torch import nn
import torchsummary

import torch
from matplotlib import pyplot as plt
from torch.nn import functional as F
from tqdm.notebook import tqdm, trange
from genaibook.core import get_device

def conv_transpose_block(in_channels, out_channels, kernel_size=3, stride=2, padding=1, output_padding=0, with_act=True):
    modules = [ nn.ConvTranspose2d(in_channels, out_channels, kernel_size=kernel_size, stride=stride, padding=padding, output_padding=output_padding)]
    if with_act:
        modules.append(nn.BatchNorm2d(out_channels))
        modules.append(nn.ReLU())
    return nn.Sequential(*modules)



class Encoder(nn.Module):
    def __init__(self, in_channels):
        super().__init__()
        self.conv1 = conv_block(in_channels, 128)
        self.conv2 = conv_block(128, 256)
        self.conv3 = conv_block(256, 512)
        self.conv4 = conv_block(512, 1024)
        self.linear = nn.Linear(1024, 16)

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = self.conv4(x)
        x = self.linear(x.flatten(start_dim=1))
        return x

class Decoder(nn.Module):
    def __init__(self, out_channels):
        super().__init__()

        self.linear = nn.Linear(16, 1024 * 4 * 4)
        self.t_conv1 = conv_transpose_block(1024, 512)
        self.t_conv2 = conv_transpose_block(512, 256, output_padding=1)
        self.t_conv3 = conv_transpose_block(256, out_channels, output_padding=1)


    def forward(self, x):
        bs = x.shape[0]
        x = self.linear(x)
        x = x.reshape(bs, 1024, 4, 4)
        x = self.t_conv1(x)
        x = self.t_conv2(x)
        x = self.t_conv3(x)
        return x
        

class AutoEncoder( nn.Module):
    def __init__(self, in_channels):
        super().__init__()
        self.encoder = Encoder(in_channels)
        self.decoder = Decoder(in_channels)

    def encode(self, x):
        return self.encoder(x)
    

    def decode(self, x):
        return self.decoder(x)


    def forward (self, x):
        return self.decode(self.encode(x))
        

class AutoEncode(nn.Module):
    def __init__(self, in_channels):
        super().__init__()
        self.encoder = Encoder(in_channels)
        self.decoder = Decoder(in_channels)

    def encode(self, x):
        return self.encoder(x)

    def decode(self, x):
        return self.decoder(x)


    def forward(self, x):
        return self.decode(self.encode(x))





def mnist_to_tensor(samples):
    t = transforms.ToTensor()
    samples["image"] = [t(image) for image in samples["image"]]
    return samples

def conv_block(in_channels, out_channels, kernel_size=4, stride=2, padding=1):
    return nn.Sequential(
        nn.Conv2d(in_channels, out_channels, kernel_size=kernel_size, stride=stride, padding=padding),
        nn.BatchNorm2d(out_channels),
        nn.ReLU(),
    )

in_channels = 1
mnist = load_dataset("ylecun/mnist")
mnist = mnist.with_transform(mnist_to_tensor)
mnist["train"] = mnist["train"].shuffle(seed=1337)
# x = mnist["train"]["image"][0]
x = mnist["train"]["image"][0][None, :]
mpl.rcParams["image.cmap"] = "gray_r"
print(x.min(), x.max())
bs = 64
train_dataloader = DataLoader(mnist["train"]["image"], batch_size=bs)
encoder = Encoder(in_channels).eval()
encoded = encoder(x)
print(encoded.shape)
batch = next (iter(train_dataloader))
encoded = Encoder(in_channels=1)(batch)
print(batch.shape,encoded.shape)
decoded_batch = Decoder(x.shape[0])(encoded)
print(decoded_batch.shape)


model = AutoEncoder(1)

print(torchsummary.summary(model, input_size = (1, 28, 28), device="cpu"))




num_epochs = 10
lr = 1e-4
device = get_device()
model = model.to(device)
optimizer = torch.optim.AdamW(model.parameters(), lr=lr, eps=1e-5)

losses = [] 

for _ in (progress := trange(num_epochs, desc="Training")):
    for _, batch in (
        inner := tqdm(enumerate(train_dataloader), total=len(train_dataloader))
    ):
        batch = batch.to(device)
        preds = model(batch)
        loss = F.mse_loss(preds, batch)
        inner.set_postfix(loss=f"{loss.cpu().item():.3f}")
        losses.append(loss.item())
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()


progress.set_postfix(loss=f"{loss.cpu().item():.3f}", lr=f"{lr:.0e}")

plt.plot(losses)
plt.xlabel("Step")
plt.ylabel("Loss")
plt.title("AutoEncoder - Training Loss Curve")


eval_bs = 18
eval_dataloader = DataLoader(mnist["test"]["image"], batch_size=eval_bs)

model.eval()
with torch.inference_mode():
    eval_batch = next(iter(eval_dataloader))
    predicted = model(eval_batch.to(device)).cpu()

batch_vs_preds = torch.cat((eval_batch, predicted))
show_images(batch_vs_preds, imsize=1, nrows=2)
plt.show()