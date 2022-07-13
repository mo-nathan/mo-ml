# mo-ml
Mushroom Observer Machine Learning Playground

Currently using Python 3.10.5.

Once that's installed you'll need to install the `pathlib` and `fastai` modules.
You can either dig into Anaconda to create a python environment or you can
just use `pip` (possibly `pip3` depending on how you have your machine configured.
Using pip you should be able to do:

`pip install pathlib fastai`

Once that's done you can get a sample of 100 images from each of 11 taxa by
running:

`./download.py mo.json`

You can tweak the taxa you get by changing labels.txt.  You can adjust the number
of files by changing the value of `obs_per_label` in download.py.

Once you have the images downloaded, you can build a model by running:

`./build_model.py`

This will run 10 epochs using the resnet34 pretrained model.

# Things worth reading

https://www.inaturalist.org/blog/63931-the-latest-computer-vision-model-updates

https://course.fast.ai/

# Goals

Minimal Viable Model for the Website
- Start with the labels from Alan Ceslestino's model
- Use resnet34
- Review Alan's Jupyter Notebooks
- Document reproducible process
- Try using Google GPU systems
- Hook it into MO using updated software (up to date Python and fastai)

Explore Model Parameters
- How do we measure "better"?
- Does image resolution change anything?
- Does the resnet change anything?
- Should we be using data augmentation?
- What happens when we looking at the last 1000 observations?

Image Review Process
- Should we add non-fungal labels like 'microscopy', 'environment', or 'junk'?
- How do we mark images for other labels (like the above or alternative taxa etc.)?
- Should we do something special with non-diagnostic images (like just the cap)?
- Can we easily create a UI for quick review of a label?
- Is a multi-label system desirable? (https://medium.com/mlearning-ai/approaching-multi-label-image-classification-using-fastai-515a4fd52c8c)

Handling Non-Species Ids
- What do we do with "Amanita gemmata group" and other "groups"?
- How can we get higher level taxa like "Agaricales" or "Russula"?
- How do we find some reasonable label for everything?

Add New Taxa
- What are the criteria?
- Can we source images for rare taxa?
- Can we find very similar taxa that maybe should be grouped? (lumping)
- Is there anyway to identify names that should get split?

Expanding the model
- Can we add location?  Seasonality?  Habitat/substrate?  Microscopic features?  DNA?
- Can we give users the ability to give feedback on bad ids?

Other features
- Can we find similar images (vs. just getting a set of labels)?
