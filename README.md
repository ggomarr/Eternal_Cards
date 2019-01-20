# Eternal Card Collection Extractor

This project was a lot of fun - it includes simulating mouse activity and taking screenshots on one end, and image feature extraction and classification (in a library of 1000+ options) on the other. Plus, it helped me continue using the great deck search offered by Eternal Warcry when Extesy's deck tracker stopped being updated. (Come back! We miss you!)

It can run either from the Jupyter notebook (20181118 Eternal card extractor v.0.5.ipynb) or through the Python 3 scripts (Collection screenshot taker v.0.5.py first to get the screenshots, and then Collection card extractor v.0.5.py to identify the cards). I would recommend the notebook because I find it easier to understand. Either method expects the library files (card_library_set_[SET_NUMBER].gz) to be available in the 'Libraries' subfolder and a subfolder called 'Screenshots' to contain the screenshots of the collection. All paths can of course be changed within the code.

A full run takes some 10 min, but I guess that is the price you pay for direct image identification.

In order to use it you will need some Python knowledge, including how to install packages and how to run Jupyter notebooks. It is not quite for the faint of heart, because the card location parameters may require some tweaking. Take it as a learning opportunity and I will do what I can to help you out, just let me know.

Enjoy, and keep playing!

Special thanks to Eternal Warcry for allowing me to use their assets!

SOME HINTS
- The scripts run on Pyhon 3; may run on Python 2, but have not checked
- A technique called SIFT is used to do the identification. cv2 versions above 3.4.2 do not seem to have xfeatures2d.SIFT methods directly available; when in doubt, force the installation of version 3.4.2.16. I used the following:
  - pip3 install --user opencv-python==3.4.2.16
  - pip3 install --user opencv-contrib-python==3.4.2.16
- The packages opencv-python and open-contrib-python seemed to be needed for SIFT to work

CHANGELOG

20190120 - v.0.5

The 0.4 version performed very badly with the new Defiance set, so I went in and reworked the tool a bit (and integrated u/Sekers' feedback - thanks!):
- Made sure the Eternal Warcry card sections used to extract features for the library and those from the screenshots were properly aligned
- Added a bit of blurring to the Eternal Warcry card sections used to extract features to better match what I was getting from the screenshots
- Split the library by card set so that none of the resulting files is too large for Github
- Added an improved screenshot comparator so that no duplicate screenshots are taken, hopefully
- Added some hints to the README
- Added an option to simulate a mouse over every card before taking sreenshots to remove the 'NEW' aura. It is disabled by default so that the script does not make any changes in your collection; if you want to use it you will need to change the remove_new_aura flag in the code from False to True
