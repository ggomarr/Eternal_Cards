import pyautogui

pyautogui.click(10,10)

for i in range(150):
  pyautogui.screenshot('ss{:03d}.png'.format(i))
  pyautogui.click(1170,400)