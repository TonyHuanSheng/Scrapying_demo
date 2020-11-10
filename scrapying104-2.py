# https://tlyu0419.github.io/2019/04/18/Crawl-JobList104/#more
# https://tlyu0419.github.io/2020/06/19/Crawler-104HumanResource/?fbclid=IwAR02X4UJlO47X6VIAeqTDoTR2T-5_vMKVMNMSk1w3mx6YFfSNUwTcMfToJc

from bs4 import BeautifulSoup
import pandas as pd
import requests
import json
import time


# [functions for open and export file]--------------------------------

def open_json_file(CACHE_FNAME):
    try:
        cache_file = open(CACHE_FNAME, 'r')
        cache_contents = cache_file.read()
        CACHE_DICTION = json.loads(cache_contents)
        cache_file.close()
        return CACHE_DICTION

    except:
        CACHE_DICTION = {}
        return CACHE_DICTION


def dump_json_file(query_dict, file_name):
    dumped_json_cache = json.dumps(query_dict)
    fw = open(file_name, "w")
    fw.write(dumped_json_cache)
    fw.close()
    print('dump the data successfully')


# [functions for web scraping ]--------------------------------

# input: parameters for 104 job search
# output: list of job post URL
def search_job_url(keyword, area, page):
    url = 'https://www.104.com.tw/jobs/search/?'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    }

    my_params = {'ro': '1',  # 限定全職的工作，如果不限定則輸入0
                 'keyword': keyword,  # 想要查詢的關鍵字
                 'area': area,  # 指定區域
                 'isnew': '30',  # 只要最近一個月有更新的過的職缺
                 'mode': 'l',  # 清單的瀏覽模式
                 'page': str(page)
                 }

    response = requests.get(url=url, params=my_params, headers=headers)
    soup_article = BeautifulSoup(response.text, 'html.parser')
    label = soup_article.select('a[class="js-job-link"]')  # locate job URL
    lst_url = [i['href'][2:].split('?')[0] for i in label]  # write URLs into a list
    print('GET URLs of page :', page) if lst_url != [] else print('URLs NOT FOUND of page :', page)
    time.sleep(2)

    return lst_url


# input: a URL of a job
# output: a dictionary from job JSON data
def get_from_url(job_url):
    end_of_url = job_url.split('/')[-1]
    full_url = "https://www.104.com.tw/job/ajax/content/" + end_of_url
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
        'Referer': 'https://www.104.com.tw/job/' + end_of_url
    }
    response = requests.get(url=full_url, headers=headers)
    print('Successfully get the data from URL: ', job_url)
    job_dict = json.loads(response.text)
    return job_dict


# input: a dictionary from job JSON data
# output: a dictionary of fetched data
def extract_from_dict(data_dict):
    data_dict = data_dict['data']
    job_dict = {}

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


def cache_or_scrapping(job_url, cache_dict, CACHE_FNAME):
    if job_url in cache_dict.keys():
        print('already have the data from URL: ', job_url)

    else:
        # fetch JSON data from one URL into a Dictionary
        data_dict = get_from_url(job_url)
        # extract data from Dictionary
        extract_dict = extract_from_dict(data_dict)
        cache_dict.update({job_url: extract_dict})
        dump_json_file(cache_dict, CACHE_FNAME)


def df_export_csv(cache_dict):
    dict_for_pd = {key: [] for key in list(cache_dict[list(cache_dict.keys())[0]].keys())}
    for key in cache_dict.keys():
        data = cache_dict[key].items()
        for k, v in data:
            dict_for_pd[k].append(v)
        print('='*20)

    # print(dict_for_pd)
    df = pd.DataFrame.from_dict(dict_for_pd)
    df.to_csv('104_job_data.csv', encoding="utf_8_sig")
    return df



def main():
    CACHE_FNAME = '104_jobs.json'  # store the cache files
    cache_dict = open_json_file(CACHE_FNAME)

    # First, get list of URLs from 104 job search page
    lst_url_1 = search_job_url('數據分析', '6001001000', 1)  # 限定在台北的工作

    # Second, get data from each URL
    for i in lst_url_1:
        job_url = i  # get one URL
        cache_or_scrapping(job_url, cache_dict, CACHE_FNAME)
        # use cache to check whether the data already exist
        # If data not exist, call function to get data from website

    # Third, export data into pandas csv
    df = df_export_csv(cache_dict)
    print(df)



if __name__ == '__main__':
    main()
