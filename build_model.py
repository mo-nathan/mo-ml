from pathlib import Path
from fastai.vision.all import get_image_files
from fastai.vision.all import ImageDataLoaders
from fastai.vision.all import Resize
from fastai.vision.all import vision_learner
from fastai.vision.all import error_rate
from fastai.vision.all import resnet34
from fastai.vision.all import SimpleNamespace
from fastai.vision.all import PILImage
from fastai.vision.all import load_learner

path = Path('sample')
fnames = get_image_files(path)
def label_func(x):
    return x.parent.name

# dls = ImageDataLoaders.from_path_func(path, fnames, label_func, item_tfms=Resize(160))
# learn = vision_learner(dls, resnet34, metrics=error_rate)
# learn.fine_tune(10)

learn = load_learner("sample/first.pkl")
learn.dls.vocab

# uploader = SimpleNamespace(data = ['sample/Coprinus_comatus/1084.jpg'])
# img = PILImage.create(uploader.data[0])
# learn.predict(img)
