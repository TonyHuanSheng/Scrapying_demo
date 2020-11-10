from lxml import etree
import grequests
import os
import json
import glob


#讀取json檔抓取url建立成list
def json_urltxt():
    path = r'C:/Users/Big data/jupyer/interior_talk_0923_ta_remix'
    all_files = glob.glob(os.path.join(path, '*.json'))
    print(all_files)
    links=[]
    for file in all_files:
        with open (file,'r',encoding='utf-8-sig') as f:
            pixnet_json=json.loads(f.read())
            #print(pixnet_json['link'])
            links.append(pixnet_json["內文"])
    print(links)
    return links


#url list 放進去後寫入txt檔
def get_txt(links):
    reqs = (grequests.get(link) for link in links)# 建立請求集合
    response = grequests.imap(reqs, grequests.Pool(5))
    #print(response)
    for i in response:
        i.encoding = 'utf-8'

        html = etree.HTML(i.content)  # 解析HTML原始碼
        txt=html.xpath('//div[@id="article-content-inner"]/p//text()')
        print(txt)
        with open("test.txt", "a",encoding='utf8') as f:
            f.writelines(txt)

def main():
    links=json_urltxt()

    with open("seatest.txt", "a", encoding='utf8') as f:
        f.writelines(links)
    #get_txt(links)


if __name__ =='__main__':
    main()

