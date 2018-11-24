# Eternal Card Collection Extractor

This project was a lot of fun - it includes simulating mouse activity and taking screenshots on one end, and image feature extraction and classification (in a library of 1000+ options) on the other. Plus, it helped me continue using the great deck search offered by Eternal Warcry when Extesy's deck tracker stopped being updated. (Come back! We miss you!)

It can run either from the Jupyter notebook (20181118 Eternal card extractor v.0.4.ipynb) or through the PYthon scripts (Collection screenshot taker.py to get the screenshots and Collection card extractor.py to identify the cards). I would recommend the notebook because I find it easier to understand. Either method expects the library file (card_library.gz) to be available in the same folder and a subfolder called Screenshots to contain the screenshots of the collection. All paths can of course be changed within the code.

A full run takes some 10 min, but I guess that is the price you pay for direct image identification.

In order to use it you will need some Python knowledge, including how to run Jupyter notebooks and how to install packages. It is not quite for the faint of heart, because the card location parameters may require some tweaking. Take it as a learning opportunity and I will do what I can to help you out, just let me know!

Enjoy, and keep playing!

Special thanks to Eternal Warcry for allowing me to use their assets!
