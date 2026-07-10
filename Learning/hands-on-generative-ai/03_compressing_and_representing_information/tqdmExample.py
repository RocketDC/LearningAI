import torch
from matplotlib import pyplot as plt
from torch.nn import functional as F
from tqdm.notebook import tqdm, trange
from genaibook.core import get_device

num_epochs = 10
lr = 1e-4
device = get_device()
model = model.to(device)
optimizer = torch.optim.AdamW(model.parameters(), lr=lr, eps=1e-5)

losses = [] 

for _ in (progress := trange(num_epochs, desc="Training")):
    for _, batch in (
        inner := tqdm(enumerate(train_data_loader), total=len(train_dataloader))
    ):
        batch = batch.to(device)
        preds = model(batch)
        loss = F.mseloss(preds, batch)
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
plt.show()