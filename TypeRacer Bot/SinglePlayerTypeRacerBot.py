import time
import pyautogui
from selenium import webdriver

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("https://play.typeracer.com")

time.sleep(4)
pyautogui.hotkey('ctrl', 'alt', 'i')
time.sleep(7)

text = driver.find_element_by_class_name("gameView").text
text = text.split("\n")
print(type(text))
print(text[-3])

time.sleep(10)
pyautogui.typewrite(text[-3], interval=0.001)
time.sleep(15)
driver.quit
