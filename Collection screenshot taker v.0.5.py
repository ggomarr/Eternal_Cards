# ## Section B: Grab screenshots of your card collection
# For this section, get Eternal running (maximized is easier) and head to the first screen of your card collection. Afterwards Alt-Tab back to the command line, make sure it is unmaximized and in a position that leaves Eternal visible on the top left corner (so that Python can simulate a click on the Eternal client and bring it to the foreground to take the screenshots), and run the code.

import pyautogui
import PIL
from PIL import ImageChops
import numpy as np
import time

screenshots_folder='./Screenshots/'
    # Where to save screenshots
max_screenshots=150
    # Stop after so many screenshots if the end condition is not met
avg_diff_cutoff=5
    # Screenshot average pixel value to consider two screenshots identical
same_img_limit=3
    # Number of identical sequential screenshots to determine the end of the collection has been reached
eternal_x,eternal_y=10,10
    # Position to click on in order to bring Eternal to the foreground
next_x,next_y=0.855*pyautogui.size()[0],0.525*pyautogui.size()[1]
    # Position to click to move to the next collection page

remove_new_aura=True
    # Flag signaling whether the shinyness around new cards should be removed
    # Before taking the screenshots
sep_x,sep_y=int(0.1218*pyautogui.size()[0]),int(0.3852*pyautogui.size()[1])
    # Represents the distances between equivalent positions of cards on the screenshot,
    # i.e., 'top left to top left' or 'center to center', or whatever
crd_x,crd_y=int(0.1730*pyautogui.size()[0]),int(0.2120*pyautogui.size()[1])
    # Represents the top left corner of the feature extraction box of the first card
pos_lst=[ (crd_x+n_x*sep_x,crd_y+n_y*sep_y)
          for n_y in range(2) for n_x in range(6) ]
    # Represent a position in each of the 12 cards so that the script can remove the 'NEW' aura

pyautogui.click(eternal_x,eternal_y)

cnt_ss=0
cnt_page=0
cnt_same=0
old_screenshot=PIL.Image.new('RGB',pyautogui.size())
while (cnt_ss<max_screenshots) and (cnt_same<same_img_limit):
    cnt_ss=cnt_ss+1
    if remove_new_aura:
        time.sleep(0.1)
        for card_x,card_y in pos_lst:
            pyautogui.moveTo(card_x,card_y)
        pyautogui.moveTo(next_x,next_y)
    new_screenshot=pyautogui.screenshot()
    if np.asarray(ImageChops.difference(old_screenshot,new_screenshot)).mean()>avg_diff_cutoff:
        cnt_same=0
        cnt_page=cnt_page+1
        new_screenshot.save(screenshots_folder+'ss{:03d}.png'.format(cnt_page))
        old_screenshot=new_screenshot
    else:
        cnt_same=cnt_same+1
    pyautogui.click(next_x,next_y)
