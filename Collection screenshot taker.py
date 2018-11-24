# ## Section B: Grab screenshots of your card collection
# For this section, get Eternal running (maximized is easier) and head to the first screen of your card collection. Afterwards Alt-Tab back to the command line, make sure it is unmaximized and in a position that leaves Eternal visible on the top left corner (so that Python can simulate a click on the Eternal client and bring it to the foreground to take the screenshots), and run the code.

import pyautogui

screenshots_folder='./Screenshots/'
    # Where to save screenshots
max_screenshots=150
    # Stop after so many screenshots if the end condition is not met
eternal_x,eternal_y=10,10
    # Position to click on in order to bring Eternal to the foreground
next_x,next_y=0.855*pyautogui.size()[0],0.525*pyautogui.size()[1]
    # Position to click to move to the next collection page 
    # next_x,next_y=1170,400 # Works well for a screen resolution of 1366 x 768

pyautogui.click(eternal_x,eternal_y)

cnt=0
old_screenshot=None
done=False
while (not done) and (cnt<max_screenshots):
    cnt=cnt+1
    new_screenshot=pyautogui.screenshot()
    if new_screenshot!=old_screenshot:
        new_screenshot.save(screenshots_folder+'ss{:03d}.png'.format(cnt))
        old_screenshot=new_screenshot
        pyautogui.click(next_x,next_y)
    else:
        done=True