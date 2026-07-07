from datasets import load_dataset
from genaibook.core import show_images
import matplotlib as mpl


ds = load_dataset("ylecun/mnist")
print(ds)
show_images(ds["train"]["image"][:4])
mpl.rcParams["image.cmap"] = "gray_r"
show_images(ds["train"]["image"][:4])
mpl.pyplot.show()



