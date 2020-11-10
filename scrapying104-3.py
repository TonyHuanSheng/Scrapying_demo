import requests #使用requests對網頁提出請求
# import dryscrape #windows無法使用
from bs4 import BeautifulSoup
import re
import time
import json

import random
# 找出 ajax/content

input = '大數據' #預設
order = 15 #下拉筆數?
page = 1 #由第一頁開始
ro = 1 # ro: 0 所有工作 1 全職 2 兼職 3 高階

Headers = dict()
Data = dict()
Json_dict = dict() #儲存成Json用的Dictionary

ss = requests.session()
Headers = {
    'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6',
    'Connection':'keep-alive',
    'Host':'www.104.com.tw',
    'Referer':'https://www.104.com.tw/jobs/main/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/84.0.4147.105 Safari/537.36'
}

Headers_page = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/84.0.4147.105 Safari/537.36',
    # 'Referer': 'https://www.104.com.tw/job/6vrlf',
    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}

# dataframe = pd.DataFrame(columns=['workid','title','content','jobTags','salary','salaryRange','jobType','addressDetail'
#             ,'mangageResp','businessTrip','workPeriod','startWorkingDay','needEmp','acceptRoles','workExp','edu'
#             ,'major','languageNeed','languageLocalneed','speciality','workskill','certificate','drivelicense','other'])

def get_work_page(url,workid,companyTitle): #前往工作頁面抓取詳細資料
    global Json_dict #宣告全域變數
    tmp_url = url.split('//')[0] + '//' + url.split('/')[2] + '/' +url.split('/')[3] + '/ajax/content/' +url.split('/')[4]
    # print(tmp_url) #json 網址處理
    ref_url = re.sub('[?].*','',url) #正規表示式
    # print(ref_url)
    Headers_page['Referer'] = ref_url
    res = requests.get(url = tmp_url, headers = Headers_page)
    a = json.loads(res.text) #取得json檔

    jsonWrite = dict()  # By workid整理成Json檔案
    jsonWrite[workid] = {'workid':workid}
    # print(jsonWrite)
    # print(a)
    # df = pd.DataFrame.from_dict(a, orient="index")
    # df.to_csv('./worklists/{}.txt'.format(workid),'w',encoding='utf8')
    # soup = BeautifulSoup(res.text,'html.parser')
    # app = soup.find_all('script',{'type':'application/ld+json'}) #用手機板可以讀取
    # print(app)
    #取得工作title
    title = a['data']['header']['jobName']
    title = re.sub('^【.*】','',title) #取代掉【地名】
    print('工作title:',title)

    jsonWrite[workid]['title'] = title
    jsonWrite[workid]['url'] = url
    jsonWrite[workid]['companyTitle'] = companyTitle #公司名稱
    # print(jsonWrite)

    #取得工作內容
    content = a['data']['jobDetail']['jobDescription']
    print(content)
    jsonWrite[workid]['content'] = content

    #取得工作類型標籤
    jobTags = list()
    for i in a['data']['jobDetail']['jobCategory']:
        jobTags.append(i['description'])
    print(jobTags)
    jsonWrite[workid]['jobTags'] = jobTags

    #工作待遇
    salary = a['data']['jobDetail']['salary']
    print(salary)
    salaryRange = str(a['data']['jobDetail']['salaryMin']) + '-' + str(a['data']['jobDetail']['salaryMax'])
    jsonWrite[workid]['salary'] = salary

    #薪資區間
    if salaryRange == '0-0': #清空
        salary_range = ''
    else:
        print(salaryRange)
    jsonWrite[workid]['salaryRange'] = salaryRange
    #工作類型
    if   ro == 1:
        jobtype = '全職'
    elif ro == 2:
        jobtype = '兼職'
    elif ro ==3:
        jobtype = '高階'
    jsonWrite[workid]['jobType'] = jobtype

    #上班地址
    addressDetail = a['data']['jobDetail']['addressRegion'] + a['data']['jobDetail']['addressDetail']
    print(addressDetail)
    jsonWrite[workid]['addressDetail'] = addressDetail

    #管理責任
    mangageResp = a['data']['jobDetail']['manageResp']
    print(mangageResp)
    jsonWrite[workid]['manageResp'] = mangageResp

    #出差外派
    businessTrip = a['data']['jobDetail']['businessTrip']
    print(businessTrip)
    jsonWrite[workid]['businessTrip'] = businessTrip

    #上班時段
    workPeriod = a['data']['jobDetail']['workPeriod']
    print(workPeriod)
    jsonWrite[workid]['workPeriod'] = workPeriod

    #可上班日
    startWorkingDay = a['data']['jobDetail']['startWorkingDay']
    print(startWorkingDay)
    jsonWrite[workid]['startWorkingDay'] = startWorkingDay

    #需求人數
    needEmp = a['data']['jobDetail']['needEmp']
    print(needEmp)
    jsonWrite[workid]['needEmp'] = needEmp

    #接受身分
    acceptRoles = list()
    for i in a['data']['condition']['acceptRole']['role']:
        acceptRoles.append(i['description'])
    print(acceptRoles)
    jsonWrite[workid]['acceptRoles'] = acceptRoles

    #工作經歷
    workExp = a['data']['condition']['workExp']
    print(workExp)
    jsonWrite[workid]['workExp'] = workExp

    #學歷
    edu = a['data']['condition']['edu']
    print(edu)
    jsonWrite[workid]['edu'] = edu

    #科系要求
    major = a['data']['condition']['major']
    if not major:
        major = '不拘'
    print(major)
    jsonWrite[workid]['major'] = major

    #語文條件
    languageNeed = dict()
    for i in a['data']['condition']['language']:
        languageNeed[i['language']] = i
    print(languageNeed) #處理成dict
    jsonWrite[workid]['languageNeed'] = languageNeed

    #當地語言
    languageLocalneed = dict()
    for i in a['data']['condition']['localLanguage']:
        languageLocalneed[i['language']] = i
    print('當地語言:',languageLocalneed)
    jsonWrite[workid]['languageLocalneed'] = languageLocalneed

    #擅長工具
    specialty = list()
    for i in a['data']['condition']['specialty']:
        specialty.append(i['description'])
    print('擅長工具:',specialty)
    jsonWrite[workid]['specialty'] = specialty

    #工作技能
    workSkill = list()
    for i in a['data']['condition']['skill']:
        workSkill.append(i)
    print('工作技能:',workSkill)
    jsonWrite[workid]['workSkill'] = workSkill

    #具備證照
    certificate = list()
    for i in a['data']['condition']['certificate']:
        certificate.append(i)
    print('具備證照:',certificate)
    jsonWrite[workid]['certificate'] = certificate
    #具備駕照
    driverLicense = list()
    for i in a['data']['condition']['driverLicense']:
        driverLicense.append(i)
    print('具備駕照:',driverLicense)
    jsonWrite[workid]['driverLicense'] = driverLicense

    #其他條件
    others = a['data']['condition']['other']
    print('其他條件:',others)
    jsonWrite[workid]['others'] = others

    #儲存Json檔案
    with open("./worklists/{}.json".format(workid), "w",encoding = 'utf-8') as outfile :
        json.dump(jsonWrite,outfile,ensure_ascii=False)

    time.sleep(random.uniform(1,2))

def get_url(url):
    # print(url) #搜尋 = 大數據
    res = ss.get(url, headers=Headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    target = soup.find('div', {'id': 'js-job-content'})  # 抓取該頁的工作清單
    # print(target)
    cnt = 0  # 計算當前筆數
    try:
        for i in target.find_all('article', {'class': re.compile('^b-block')}):
            #工作號碼 << 用來當作pri key
            workid = i['data-job-no']
            print('工作號碼',i['data-job-no'])
            #頁面連結
            link = i.find('a', {'class': 'js-job-link'})['href']  # 取得連結
            link = 'https://' + link.replace('//', '')  # 刪除前置slash
            # link = link.replace('www', 'm')  # 轉成手機板 目前是正解 08/03 嘗試其他方法
            print('前往:',link)
            companyTitle = i.find('ul',{'class':'b-list-inline b-clearfix'}).find('a').text.strip()
            print(companyTitle)
            #前往網站
            get_work_page(link,workid,companyTitle)
            # time.sleep(30)

        else: #迴圈順利跑完時 帶入後15筆
            global page
            page += 1
            next_page = '''
https://www.104.com.tw/jobs/search/?ro=0&keyword=%{input}&jobcatExpansionType=0&
jobsource=2018indexpoc&ro={ro}&order={order}&page={page}
'''.format(input = input,ro = ro,order= order, page =page)
            get_url(next_page) #前往下一頁
    except AttributeError:
        #程式結束
        exit


url = '''
https://www.104.com.tw/jobs/search/?ro=0&keyword=%{input}&jobcatExpansionType=0&
jobsource=2018indexpoc&ro={ro}&order={order}&page={page}
'''.format(input = input,ro = ro,order= order, page =page)

get_url(url)


##########################備註區
#dryscrape 也可以運行JS檔案但僅能在以下系統執行
#Mac OS X 10.9 Mavericks and 10.10 Yosemite
#Ubuntu Linux
#Arch Linux
##########################