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

# Additional questions

What happens with more taxa?

What happens with other resnets?

Can we figure out what Alan Celestino did? (1219 taxa, not sure which images)
(I have some Jupyter Notebooks from Alan)

Do we need a service with a GPU to get the above to fly?

Will that include the Amanita gemmata group?

How do we deal with higher level taxa? (genera, families etc.)

Can we handle rare species well maybe using data augmentation?

Is there a good way to coalesce very similar taxa?

Can we spot interesting new things to name? (groups of similar species or
perhaps species that have internal clusters that might be deserve new names)

What's a good strategy for providing some sort of label for everything?  (What do
we do with "Agaricales"?)

How can we add location, seasonability and/or habitat/substrate info?

Can we find similar images (vs. just getting a set of labels)?

How do we use "bad" ids as feedback?

How/when do we add new taxa?
