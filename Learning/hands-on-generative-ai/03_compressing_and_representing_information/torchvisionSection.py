from torchvision import transforms
from datasets import load_dataset
from genaibook.core import show_images
import matplotlib as mpl
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader

def mnist_to_tensor(samples):
    t = transforms.ToTensor()
    samples["image"] = [t(image) for image in samples["image"]]
    return samples

mnist = load_dataset("ylecun/mnist")
mnist = mnist.with_transform(mnist_to_tensor)
mnist["train"] = mnist["train"].shuffle(seed=1337)
x = mnist["train"]["image"][0]
mpl.rcParams["image.cmap"] = "gray_r"
print(x.min(), x.max())
show_images(mnist["train"]["image"][0])
plt.show()
bs = 64
train_dataloader = DataLoader(mnist["train"]["image"], batch_size=bs)
