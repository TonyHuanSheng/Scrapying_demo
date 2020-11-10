from lxml import etree
import requests
from http import cookiejar
from bs4 import BeautifulSoup
import time
import re
import os
import json


#取得HTML
def lxml_html(url):
    headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"
         ,"referer": "https://www.ikea.com.tw/zh/products/beds/bed-frames/askvoll-spr-59030509"}
    cookies=cookiejar.CookieJar()
    #print(cookies)
    res=requests.get(url=url,headers=headers,cookies=cookies)
    #res.encoding=res.apparent_encoding #自動轉換代碼
    #關鍵字charse 找網頁編碼格式

    html=etree.HTML(res.text)
    return html

#轉json檔寫入指定路徑資料夾內
def dump_json_file(query_dict,file_name,resource_path):
    with open(resource_path+"/{}.json".format(file_name),'w',encoding='utf-8') as outfile:
            json.dump(query_dict,outfile,ensure_ascii=False)
            print('dump the data successfully')


# 建立指定路徑資料夾
def set_folders(keys):
    resource_path = r'./IKEAFolders/' + keys
    if not os.path.exists(resource_path):
        os.makedirs(resource_path)
    else:
        print(resource_path)
        return resource_path


# 取得key值組成的所有url頁數網址
def GetRedisUrl(keys):
    set_folders(keys)
    url = "https://www.ikea.com.tw/zh/products/" + keys
    print(url)
    get_All(url, keys)

    while True:
        try:
            html_lxml = lxml_html(url)
            page_url = html_lxml.xpath("//a[@class='page-link']/@data-sitemap-url")[0]
            print(page_url)
            get_All(page_url, keys)
            url = page_url

        except IndexError:
            break
    print("End of program")


# 取造訪頁面所有所需資訊
def get_All(url, keys):
    resource_path = set_folders(keys)

    html_lxml = lxml_html(url)
    # url list
    url_beds = html_lxml.xpath('//div[@class="card-header"]/a/@href')
    # print(url_beds)
    # title list
    title_list = html_lxml.xpath('//h6[@class="display-7"]/text()')

    # summary list
    title_summary_list = html_lxml.xpath('//span[@class="itemFacts"]/text()')
    # price list
    price_list = html_lxml.xpath('//div[@class="itemPrice-wrapper"]//span/text()')
    # type
    title_type = url.split('/')[5]

    for u in range(len(title_list)):
        try:
            # 商品網址
            bedsurl = "https://www.ikea.com.tw" + url_beds[u]
            # print(bedsurl)

            # 取得html
            in_html = lxml_html(bedsurl)

            # 商品ID
            title_id = ('ikea' + str((in_html.xpath('//p[contains(text(),"產品編號:")]/text()')[0]).split()[1]))  # ikea+商品編號
            # print(title_id)

            # 商品名稱
            title = title_list[u]

            # 商品編號
            title_number = in_html.xpath('//p[@class="partNumber"]/text()')

            # 商品概要
            title_summary = title_summary_list[u]

            # 商品顏色
            title_colour = title_summary_list[u].split(',')[1]

            # 商品價格
            price = price_list[u]

            # 商品照片網址
            img_jpglist = []
            img_jpg_url = in_html.xpath('//a[@class="slideImg"]/@href')
            for i in img_jpg_url:
                img_jpg = "https://www.ikea.com.tw" + i.replace('S3', "S5")
                img_jpglist.append(img_jpg)

            # 取得商品詳細標題
            beds_title = in_html.xpath('//div[@class="tab-pane_box"]/h3/text()')
            # print(beds_title)

            # 取得商品資訊
            beds_features = in_html.xpath('//div[@class="tab-pane_box"]/p/text()')

            # youknow
            youknow = []
            you_know_list = in_html.xpath('//*[@id="pills-good"]/div//.//text()')
            for j in you_know_list:
                if j == '\n' or '':
                    continue
                youknow.append(j)
            # print(youknow)

            # Material
            Material = []
            Material_list = in_html.xpath('//*[@id="pills-environment"]/div[2]//.//text()')
            for i in Material_list:
                if i == '\n' or '':
                    continue
                Material.append(i)
            # 取得產品尺寸
            beds_faangle_list = in_html.xpath('//div[@class="tab-pane_box"]/table//td/text()')
            # print(beds_faangle_list)
            beds_faangle = []
            for i in beds_faangle_list:
                if i == '\n' or '':
                    continue
                beds_faangle.append(i)
            # print(beds_faangle)

            # 設置Dict
            object_json = {'id': title_id,
                           "type": title_type,
                           'title': title,
                           "Product number": title_number[0],
                           'colour': title_colour,
                           "images": img_jpglist,
                           "summary": title_summary,
                           'price': price,
                           "url": bedsurl,
                           'Product Information': [{beds_title[0]: beds_features}],
                           'size': [{beds_title[1]: beds_faangle}],
                           'You know': youknow,
                           'Material': Material
                           }

            # 寫入json
            dump_json_file(object_json, title_id, resource_path)
        except Exception :
            pass

# 主執行程式
def main():
    kesy_list = ['sofas/fabric-sofas','sofas/leather-sofas','sofas/sofa-beds','sofas/armchairs' #沙發

]
    for i in kesy_list:
            GetRedisUrl(i)


'''
"beds/double-beds", "beds/single-beds", "beds/day-beds", "beds/loft-beds-and-bunk-beds",  # 床
                 "work-chairs", "sofas/footstools", "dining-seating/chairs-incl-covers-folding-chairs",
                 "dining-seating/stools-incl-covers", "dining-seating/bar-stools-incl-covers",  # 椅子
                 "coffee-and-side-table/sofa-tables", "work-desks", "dining-tables/tables"dining-tables/dining-set",
                 "dining-tables/high-tables", "chests-and-other-furniture/dressing-tables",
                 "chests-and-other-furniture/bedside-tables"",  # 桌子

'''



if __name__ =='__main__':
    main()