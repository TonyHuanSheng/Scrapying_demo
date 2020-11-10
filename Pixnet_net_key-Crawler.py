from lxml import etree
from bs4 import BeautifulSoup
import requests
import os
import json


#爬取URL
def get_json(url):
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
         ,"referer": "https://www.pixnet.net/tags/IKEA?filter=comments&sort=latest"}
    res=requests.get(url=url,headers=headers)
    pixnt=json.loads(res.text)
    return pixnt


#轉json檔寫入指定路徑資料夾內
def dump_json_file(query_dict,file_name,resource_path):
    with open(resource_path+"/{}.json".format(file_name),'w',encoding='utf-8') as outfile:
            json.dump(query_dict,outfile,ensure_ascii=False)
            print('dump the data successfully')


#建立指定路徑資料夾
def set_folders(resource_path):
    if not os.path.exists(resource_path):
        os.makedirs(resource_path)
    else:
        print(resource_path)


#建立指定路徑資料夾
def set_folders(resource_path):
    if not os.path.exists(resource_path):
        os.makedirs(resource_path)
    else:
        print(resource_path)


def main():
    keyslist = ['IKEA', '室內裝潢', '裝潢', '家具', '軟裝潢', '空間', '空間陳列', '家具家飾', '新家', '家','工業風','現代風','海洋風','奢華風','北歐風','鄉村風']
    resource_path = r'./Pixnet'
    set_folders(resource_path)
    for key in keyslist:
        i = 1
        while True:

            url = "https://www.pixnet.net/mainpage/api/tags/" + key + "/feeds?page=%s&per_page=20" % i + "&filter=articles&sort=latest&refer=https%3A%2F%2Fwww.pixnet.net%2Ftags%2FIKEA%3Futm_source%3DPIXNET%26utm_medium%3Dnavbar%26utm_term%3Dsearch_result_tag%26utm_content%3DIKEA"
            print(url)
            pixnt = get_json(url)

            if i <= (pixnt['data']['total_feeds'] / 20):
                print(pixnt['data']['total_feeds'])
                for j in range(len(pixnt['data']['feeds'])):
                    pixntid = pixnt['data']['feeds'][j]['member_uniqid']
                    title = pixnt['data']['feeds'][j]['title']
                    link = pixnt['data']['feeds'][j]['link']
                    images = pixnt['data']['feeds'][j]['images_url']
                    tags = pixnt['data']['feeds'][j]['tags']
                    pixnet_json = {'id': pixntid, 'title': title, 'link': link, 'images': images, 'tags': tags}

                    dump_json_file(pixnet_json, pixntid, resource_path)
            else:
                break

            i += 1


if __name__ =='__main__':
    main()