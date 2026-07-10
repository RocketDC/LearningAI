import torch.nn as nn
import torch
import matplotlib as mpl
from matplotlib import pyplot as plt
from genaibook.core import get_device
from tqdm.notebook import tqdm, trange
from torch.utils.data import DataLoader


device = get_device()
train_dataloader = DataLoader(mnist["train"]["image"], batch_size=bs)
class Encoder(nn.Module):
    def __init__(self, in_channels, latent_dims):
        super().__init__()

        self.conv_layers = nn.Sequential(
            conv_block(in_channels, 128),
            conv_block(128, 256),
            conv_block(256, 512),
            conv_block(512, 1024),

            
        )
        self.linear = nn.Linear(1024, latent_dims)

    def forward(self, x):
        bs = x.shape[0]
        x = self.conv_layers(x)
        x = self.linear(x.reshape(bs, -1))
        return x

class Decoder(nn.Module):
    def __init__(self, out_channels, latent_dims):
        super().__init__()

        self.linear = nn.Linear(latent_dims, 1024 * 4 * 4)
        self.t_conv_layers = nn.Sequential(
            conv_transpose_block(1024, 512),
            conv_transpose_block(512, 256, output_padding=1),
            conv_transpose_block(256, out_channels, output_padding=1, with_act=False),
        )
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        bs = x.shape[0]
        x = self.linear(x)
        x = x.reshape((bs, 1024, 4, 4))
        x = self.t_conv_layers(x)
        x = self.sigmoid(x)
        return x

class AutoEncoder(nn.Module):
    def __init__(self, in_channels, latent_dims):
        super().__init__()
        self.encoder = Encoder(in_channels, latent_dims)
        self.decoder = Decoder(in_channels, latent_dims)


    def encode(self, x):
        return self.encoder(x)
    
    def decode(self, x):
        return self.decoder(x)



    def forward(self, x):
        return self.decode(self.encode(x))


def train (model, num_epochs=10, lr=1e-4):
    optimizer = torch.optim.AdamW(model.parameters(), lr = lr, eps=1e-5)
    model.train()
    losses = []
    for _ in (progress:= trange(num_epochs, desc="Training")):
        for _, batch in (
            inner := tqdm(
                enumerate(train_dataloader), total=len(train_dataloader)
            )
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
    
    return losses
