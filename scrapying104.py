from bs4 import BeautifulSoup
import pandas as pd
import requests
import json
import time
from multiprocessing import Pool
from itertools import combinations_with_replacement # https://codertw.com/%E7%A8%8B%E5%BC%8F%E8%AA%9E%E8%A8%80/364249/


# [functions for open and export file]--------------------------------

def open_json_file(CACHE_FNAME): #讀取程式
    try:
        cache_file = open(CACHE_FNAME, mode='r') #開啟檔案,讀取模式
        cache_contents = cache_file.read()  #讀取檔案
        CACHE_DICTION = json.loads(cache_contents) #轉成json檔
        cache_file.close()    #關閉檔案
        return CACHE_DICTION  #回傳檔案

    except:
        CACHE_DICTION = {}
        return CACHE_DICTION


def dump_json_file(query_dict, file_name): #寫入程式
    dumped_json_cache = json.dumps(query_dict)
    print(dumped_json_cache)
    fw = open(file_name, "a")
    fw.write(dumped_json_cache)
    fw.close()
    #print('dump the data successfully')


# [functions for web scraping ]--------------------------------


# get all url
def get_from_url(job_url):
    full_url = job_url
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
        'Referer': 'https://www.104.com.tw/job/'
    }
    response = requests.get(url=full_url, headers=headers)
    #print('Successfully get the data from URL: ', job_url)
    job_dict = json.loads(response.text)
    return job_dict


# input: a dictionary from job JSON data
# output: a dictionary of fetched data
def extract_from_dict(data_dict):
    job_dict = {}
    try:
        data_dict = data_dict['data']

        # job title
        job_dict['jobName'] = data_dict['header']['jobName']
        job_dict['appearDate'] = data_dict['header']['appearDate']

        # company detail
        job_dict['companyName'] = data_dict['header']['custName']
        job_dict['companyUrl'] = data_dict['header']['custUrl']
        job_dict['industry'] = data_dict['industry']
        job_dict['addressRegion'] = data_dict['jobDetail']['addressRegion']
        job_dict['longitude'] = data_dict['jobDetail']['longitude']
        job_dict['latitude'] = data_dict['jobDetail']['latitude']

        # condition
        job_dict['acceptRole'] = data_dict['condition']['acceptRole']
        job_dict['workExp'] = data_dict['condition']['workExp']
        job_dict['edu'] = data_dict['condition']['edu']
        job_dict['major'] = data_dict['condition']['major']
        job_dict['language'] = data_dict['condition']['language']
        job_dict['skill'] = data_dict['condition']['skill']
        job_dict['certificate'] = data_dict['condition']['certificate']
        job_dict['other'] = data_dict['condition']['other']

        # job Detail
        job_dict['jobDescription'] = data_dict['jobDetail']['jobDescription']
        job_dict['jobCategory'] = data_dict['jobDetail']['jobCategory']
        job_dict['jobType'] = data_dict['jobDetail']['jobType']
        job_dict['manageResp'] = data_dict['jobDetail']['manageResp']
        job_dict['businessTrip'] = data_dict['jobDetail']['businessTrip']
        job_dict['workPeriod'] = data_dict['jobDetail']['workPeriod']
        job_dict['vacationPolicy'] = data_dict['jobDetail']['vacationPolicy']
        job_dict['startWorkingDay'] = data_dict['jobDetail']['startWorkingDay']
        job_dict['needEmp'] = data_dict['jobDetail']['needEmp']

        # salary
        job_dict['salary'] = data_dict['jobDetail']['salary']
        job_dict['salaryMin'] = data_dict['jobDetail']['salaryMin']
        job_dict['salaryMax'] = data_dict['jobDetail']['salaryMax']
        job_dict['salaryType'] = data_dict['jobDetail']['salaryType']
        job_dict['welfare'] = data_dict['welfare']['welfare']

        return job_dict
    except Exception as e:
        return job_dict

def cache_or_scrapping(job_url, cache_dict, CACHE_FNAME):
    if job_url in cache_dict.keys(): #檢查URL有沒有出現在json.keys內
        print('already have the data from URL: ', job_url)

    else:
        # fetch JSON data from one URL into a Dictionary
        data_dict = get_from_url(job_url) #呼叫get_from_url 函式
        # extract data from Dictionary
        extract_dict = extract_from_dict(data_dict) #呼叫extract_from_dict函式
        cache_dict.update({job_url: extract_dict})
        #print(type(cache_dict))
        #print(cache_dict)
        dump_json_file(cache_dict, CACHE_FNAME)


def main(a): # main(a) 內為list各項目
    CACHE_FNAME = '104_jobs.json'  # store the cache files #指定快取名稱
    cache_dict = open_json_file(CACHE_FNAME) #呼叫函式 帶入變數

    for i in combinations_with_replacement("0123456789abcdefghijklmnopqrstuvwxyz", 4): #重複組合項目0內的元素,生成4個
        job_url = "https://www.104.com.tw/job/ajax/content/" +str(a) + str(''.join(map(str, i))) # i字元轉為str,join後再轉str 組合成URL
        cache_or_scrapping(job_url, cache_dict, CACHE_FNAME) #將參數帶入function 內
        #print(job_url)
        # Third, export data into pandas csv


if __name__ == '__main__':

    list1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,'a','b']
    p =Pool(12) #開啟12進程
    p.map(main,iterable=(list1)) # map(function,iterable) list帶進main function 內