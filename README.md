## Brain Tumor Image Segmentation project

2602119096 - Thomas Gozalie

2602082515 - Christian Aldrich Mintaraga

2602065774 - Gabriel Seemore Gunawan

Dataset used: https://www.kaggle.com/datasets/mateuszbuda/lgg-mri-segmentation


## Requirements: (what we used in .venv)

filelock          3.16.1

fsspec            2024.10.0

Jinja2            3.1.4

MarkupSafe        3.0.2

mpmath            1.3.0

networkx          3.4.2

numpy             2.2.0

opencv-python     4.10.0.84

pillow            11.0.0

pip               24.3.1

pygame            2.6.1

setuptools        75.6.0

sympy             1.13.1

torch             2.5.1

torchvision       0.20.1

typing_extensions 4.12.2

## Instructions

The dataset folder for one patient can be downloaded here: https://drive.google.com/drive/folders/1NVYibM22D4am0bSzBuObzrp0TwdHZR4k
Clone the project and run App.py, where a pygame window will show up on your screen.

### Using U-Net/DeepLab

If you intend to use those deep learning models, please download the model weights here: https://drive.google.com/drive/folders/1NVYibM22D4am0bSzBuObzrp0TwdHZR4k

Once downloaded, put each file in the "utils" folder.

### Using Watershed/Region-Growing

Segmentation requires user input (semi-automatic). When "Segment" button is clicked, a new window will be spawned containing a brain tumor image, where the user needs to "draw" on the image to choose the components/starting seed for segmentation.


