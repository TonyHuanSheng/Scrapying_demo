import requests
from http import cookiejar
from lxml import etree
import os
import json
from multiprocessing import Process,Pool
import re

#轉換網頁Html
def lxml_html(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
        , 'referer': 'https://c-h-c.com.tw/shop/'}

    cookies=cookiejar.CookieJar()
    #print(cookies)
    res=requests.get(url=url,headers=headers,cookies=cookies)
    #res.encoding=res.apparent_encoding #自動轉換代碼
    #關鍵字charse 找網頁編碼格式

    html=etree.HTML(res.text)
    return html

#建立指定路徑資料夾
def set_folders(key):
    resource_path=r'./CHCCFolders/'+key+'/'
    if not os.path.exists(resource_path):
        os.makedirs(resource_path)
    else:
        print(resource_path)
    return resource_path


# 轉json檔寫入指定路徑資料夾內
def dump_json_file(query_dict, file_name, resource_path):
    with open(resource_path + "/{}.json".format(file_name), 'w', encoding='utf-8') as outfile:
        json.dump(query_dict, outfile, ensure_ascii=False)
        print('dump the data successfully')

#取得網頁所以的主題網址
def GetUrls():
    url='https://c-h-c.com.tw/shop/'
    html=lxml_html(url)
    urls_list = html.xpath('//li[@class="mega-menu-column mega-menu-columns-2-of-12"]/ul/li/a/@href')
    title_list = html.xpath('//li[@class="mega-menu-column mega-menu-columns-2-of-12"]/ul/li/a/text()')
    CHClist = []
    for run in range(len(title_list)):
        CHCdict = {'id': run, 'title': title_list[run], 'url': urls_list[run]}
        CHClist.append(CHCdict)
    content_all = []
    for number in range(len(CHClist)):
        title = CHClist[number]['title']
        in_url = CHClist[number]['url']

        htmls = lxml_html(in_url)
        content_url = htmls.xpath('//div[@class="un-product-thumbnail"]/a/@href')
        content_json = {'id':number,'title': title, 'url': content_url}
        dump_json_file(content_json,number,r'./CHCCFolders/')
        content_all.append(content_json)

    return content_all


#取得主題網頁後所有商品
def Get_ALL(content_all):
    for urls in range(len(content_all)):
        title = re.sub(r'\W', '', content_all[urls]['title'])
        urllist = content_all[urls]['url']
        path = set_folders(title)
        for url in urllist:
            content_html = lxml_html(url)

            # Name
            Name = re.sub(r'\W', '', content_html.xpath('//h1[@class="product_title entry-title"]/text()')[0])

            # Url
            Url = url
            # Price
            Price = content_html.xpath('//p/ins/span[@class="woocommerce-Price-amount amount"]/text()')
            if Price == []:
                Price = content_html.xpath('//p/span[@class="woocommerce-Price-amount amount"]/text()')
            print(Name, Url, Price)

            # Store & Brand
            Store_Brand = content_html.xpath(
                '//div[@class="summary entry-summary"]/div[@class="woo-short-description"]/p/text()')
            if Store_Brand == []:
                Store_Brand = content_html.xpath(
                    '//div[@class="summary entry-summary"]/div[@class="woo-short-description"]//span/text()')
                if Store_Brand == []:
                    pass
            else:
                # Store
                Store = Store_Brand[0]
                print('Store:', Store)
                try:
                    # Brand
                    Brand = re.sub(r'\n', '', Store_Brand[1])

                except:
                    Brand = []
                print('Brand:', Brand)
            # Introduction
            Introduction = content_html.xpath('//div[@class="wpb_wrapper"]//p[@style="text-align: center"]/text()')
            if Introduction == []:
                Introduction = content_html.xpath('//div[@class="wpb_wrapper"]//p/text()')
            print('Introduction:', Introduction)
            try:
                # size
                size = [content_html.xpath('//div[@class="wpb_wrapper"]/h4/text()')[0]
                    , content_html.xpath('//*[@id="specification"]/div[2]/div/div/div/div/div[1]//p/text()')[0]]
            except IndexError:
                size = []
                if size == []:
                    try:
                        size = [content_html.xpath('//div[@class="wpb_wrapper"]/h4/text()')[0]
                              , content_html.xpath('//div[@class="wpb_text_column wpb_content_element "]/div[@class="wpb_wrapper"]/p/text()')[1]]
                    except IndexError:
                        size = []
                        if size == []:
                            try:
                                size = [content_html.xpath('//div[@class="wpb_wrapper"]/h4/text()')[0]
                                      , content_html.xpath('//div[@class="wpb_text_column wpb_content_element "]/div[@class="wpb_wrapper"]//p//text()')[0]]
                            except IndexError:
                                size = []
                                if size == []:
                                    size = content_html.xpath('//div[@class="wpb_wrapper"]/h5/text()')
                                    if size == []:
                                        size = content_html.xpath('//div[@class="wpb_wrapper"]/h4/text()')
                                        if size == []:
                                            size = content_html.xpath(
                                                '//*[@id="1569206830467-b09ae596-da49"]/div[2]/div[1]/div/div/div/p/span/text()')
                                            if size == []:
                                                size = content_html.xpath('////*[@id="specification"]/div[2]/h4/text()')
            print('size:', size)

            # Product
            Product_img = content_html.xpath('//a[@class="photoswipe"]/img/@src')[0]
            print(Product_img)
            # Layout
            Layout_img = content_html.xpath('//div[@class="wpb_wrapper"]//img/@src')
            print(Layout_img)
            print()

            content_json = {'title': title, 'Name': Name, 'Price': Price, 'Url': Url, 'Store': Store, 'Brand': Brand,
                            'Introduction': Introduction
                , 'Product': Product_img, 'Layout': Layout_img}
            print(content_json)
            print('--')
            dump_json_file(content_json, Name, path)

def main():
     content_all=GetUrls()

     Get_ALL(content_all)


if __name__ =='__main__':
    main()