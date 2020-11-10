from bs4 import BeautifulSoup
import requests
from selenium.webdriver import Chrome
import time
import os
'''
啟動Chrome瀏覽器：
from selenium import webdriver 
browser = webdriver.Chrome() 
browser.get('http://www.baidu.com/')


啟動Firefox瀏覽器：
from selenium import webdriver 
browser = webdriver.Firefox() 
browser.get('http://www.baidu.com/')

啟動IE瀏覽器：
from selenium import webdriver 
browser = webdriver.Ie() 
browser.get('http://www.baidu.com/')
'''
local_path='imgs'

url="https://www.shutterstock.com/zh-Hant/category/interiors"
xpath='div[@id="content"]'

driver=Chrome(r'./chromedriver')


driver.get(url)
time.sleep(5)


c = driver.find_elements(xpath)

print(c)


driver.close()