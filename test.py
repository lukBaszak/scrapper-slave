from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

time.sleep(2)
chrome = webdriver.Remote(
          command_executor='http://172.18.0.2:4444/wd/hub',
          desired_capabilities=DesiredCapabilities.CHROME)

chrome.get('https://www.google.com')
print(chrome.title)

