# import dryscrape #windows無法使用
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import random
import re
import time
#from PIL import Image,ImageEnhance
# import pytesseract #讀取驗證碼 #需安裝tesseract , pip install tesseract
import time
from  selenium.common.exceptions import StaleElementReferenceException as SeleinumExc
#selenium.common常見exceptions異常
def get_timestamps():
    # 產生時間戳記
    dt = time.strftime('%Y-%m-%d %H:%M:%S')  # 時間戳記
    return dt
from selenium.webdriver.common.by import By

#驗證碼圖片儲存路徑
screenImg = "./Tmp_img/screenImg.png"
screenImg2 = "./Tmp_img/screenImg2.png"

#設定執行檔路徑
# pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\Tesseract-OCR\tesseract.exe'

#大量下載圖片
def get_start(url):
    try:
        driver = Chrome('./chromedriver.exe')
        driver.get(url)
        #找'掛號'類標籤
        c = driver.find_elements(By.XPATH, '//img[@class="z_h_9d80b z_h_2f2f0"]')
        for i in c:
            i.click()

        # c = driver.find_elements_by_class_name('z_h_9d80b z_h_2f2f0')
    except SeleinumExc:
        return 0


url = 'https://www.shutterstock.com/zh-Hant/search/%E5%AE%A4%E5%85%A7%E8%A8%AD%E8%A8%88?kw=shutterstock&c3apid' \
      't=p15867520243&gclid=CjwKCAjwj975BRBUEiwA4whRB27IIJRhDpQ2LLcEKSEQ6kWoLJdAvei4A8rSxIDgpb7lfPM4G4ripxoCF9AQAvD_BwE&gclsrc=aw.ds' #測試用
# url = 'https://app.tzuchi.com.tw/tchw/OpdReg/DtQuery.aspx?dtno=63001&Loc=dl'
# while 1:
get_start(url)


#備註區###########################################################
# python+selenium+Chromedriver使用location定位元素坐標偏差
# 使用xpath定位元素，用.location獲取坐標值，截取網頁截圖的一部分出現偏差。
#
# 之所以會出現這個坐標偏差是因為windows系統下電腦設置的顯示縮放比例造成的，location獲取的坐標是按顯示100%時得到的坐標，而截圖所使用的坐標卻是需要根據顯示縮放比例縮放后對應的圖片所確定的，因此就出現了偏差。
# 解決這個問題有三種方法：
#1.修改電腦顯示設置為100%。這是最簡單的方法；
#2.縮放截取到的頁面圖片，即將截圖的size縮放為寬和高都除以縮放比例后的大小；
#3.修改Image.crop的參數，將參數元組的四個值都乘以縮放比例。

#tesseract無法安裝時
#1. Install tesseract using windows installer available at: https://github.com/UB-Mannheim/tesseract/wiki
#2. Note the tesseract path from the installation.Default installation path at the time the time of this edit was: C:\Users\USER\AppData\Local\Tesseract-OCR. It may change so please check the installation path.
#3. pip install pytesseract
#4. Set the tesseract path in the script before calling image_to_string:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Users\USER\AppData\Local\Tesseract-OCR\tesseract.exe'
#參考
#https://stackoverflow.com/questions/50951955/pytesseract-tesseractnotfound-error-tesseract-is-not-installed-or-its-not-i

#無法成功識別
#需使用CNN (Convolutional Neural Network，卷積神經網絡)或者 RNN (Recurrent Neural Network，循環神經網絡)
#訓練出自己的識別庫。