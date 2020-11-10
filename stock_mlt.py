import requests
from bs4 import BeautifulSoup
import json
import os
import pandas

import os, time, random
from multiprocessing import Process, Pool
import multiprocessing as mp
from itertools import combinations_with_replacement


# 取得HTML
def get_html(url, headers):
    ss = requests.session()
    res = ss.get(url=url, headers=headers)
    res.encoding = res.apparent_encoding  # 自動轉換代碼
    # 關鍵字charse 找網頁編碼格式
    # print(ss.cookies)
    soup = BeautifulSoup(res.text, "html.parser")
    return soup


def set_folders():
    resource_path = r'./scotk-img'
    if not os.path.exists(resource_path):
        os.mkdir(resource_path)
    headers = {"Referer": "https://www.shutterstock.com/zh-Hant/search/interiors"
        ,
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36"
               }
    return headers


def main(page, headers):
    # for i in range(limit): # 100 -> 3 pages
    print('開始第{}頁爬蟲'.format(page))
    # for i in range(limit,limit+1): #只跑一頁
    C = time.time()
    html = get_html("https://www.shutterstock.com/zh-Hant/search/interiors?page=%s" % (page)
                    , headers
                    )
    # print(html.select(""))
    a_url = html.select('a[class=z_h_81637]')
    img_file = 1
    for i in a_url:
        # 每次重置

        json_dict = {}  # json字典格
        json_label = []  # 標籤list
        # 圖片key
        img_key = 'ssk' + str(page).zfill(6) + str(img_file).zfill(3)
        # 圖片id
        img_id = (json.loads(i.get('data-track-value'))['id'])
        # print(i)

        # 圖片jpg檔
        img_jpg = "https://image.shutterstock.com/image-illustration/corner-modern-kitchen-white-walls-600w-%s.jpg" % (
        json.loads(i.get('data-track-value'))['id'])
        # print(img_jpg)

        # 圖片網址
        img_url = ("https://www.shutterstock.com/" + i['href'])
        # print(img_url)

        # 圖片標題
        img_title = (i.select("img")[0]['alt'])
        # print(img_world)

        in_html = get_html(img_url, headers)
        # print(in_html.select('div[class="m_g_4f6b9 C_a_8cee0 section-spacing-bottom"]')[0])

        # 圖片標籤
        in_word_all = in_html.select('div[class="C_a_03061"]')[0]
        in_word_a = (in_word_all.select('a'))
        for i in in_word_a:
            json_label.append(i.text)
            # print(json_label)

        # 放入字典內
        json_dict = {"img_key": img_key, 'img_id': img_id, 'img_jpg': img_jpg, "url": img_url, "title": img_title,
                     "label": json_label}
        print('下載檔案:', img_id)
        # 轉換格式
        with open("./scotk-img/{}.json".format(img_key), "w", encoding='utf-8') as outfile:
            json.dump(json_dict, outfile, ensure_ascii=False)
        img_file += 1
        D = time.time()
        print(D - C)
    E = time.time()
    print(E - C)


''''''


def get_config(name, page, configMode):
    if not os.path.exists(r'./poolconfig'):
        os.mkdir(r'./poolconfig')
        if configMode == 'W':  # 寫入當前頁數
            with open(r"./poolconfig/{}.txt".format(), "w", encoding='utf-8') as w:
                w.write(page)
        elif configMode == 'R':  # 讀取頁數
            with open(r"./poolconfig/{}.txt".format(), 'w', encoding='utf-8') as r:
                r.readline()  # 只有一行


def run_task(name, page):
    print('Task %s (pid=%s) is running...' % (name, os.getpid()))
    main(page, set_folders())  # 每個task跑1頁
    print('Task %s end.' % name)


if __name__ == '__main__':
    while 1:
        name = 'TonyConfig'
        if not os.path.exists(r'./poolconfig'):
            os.mkdir(r'./poolconfig')
        if not os.path.exists(r'./poolconfig/{}.txt'.format(name)):
            page = 1
            with open(r"./poolconfig/{}.txt".format(name), "w", encoding='utf-8') as w:
                w.write(str(page))  # 寫入頁數
        else:
            with open(r"./poolconfig/{}.txt".format(name), 'r', encoding='utf-8') as r:
                page = r.readline()  # 取得當前頁數
        print('PAGE:', page)
        p = mp.Pool()  # 初始化pool
        mp.freeze_support()  # Windows 平台避免 RuntimeError
        cpus = mp.cpu_count()
        for i in range(0, cpus):  # 產生cpu數量的pool
            print('Current process %s.' % os.getpid())
            p.apply_async(run_task, args=(i, int(page) + i,))  # apply_async 異部執行 每個pool跑100頁
            print('Waiting for all subprocesses done...')
        page = int(page) + cpus - 1
        p.close()
        # join()方法會等待所有子進程執行完畢，調用之前必須先調用close()方法
        # 調用close()之後就不能繼續添加新的Process了
        p.join()
        # 回寫當前頁數
        with open(r"./poolconfig/{}.txt".format(name), "w", encoding='utf-8') as w:
            w.write(str(page))  # 寫入頁數
        print('All subprocesses done.')

