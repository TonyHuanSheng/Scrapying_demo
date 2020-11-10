import pandas as pd
from bs4 import BeautifulSoup
import re
import time
import json
import pandas as pd
import random
import glob
import ast  #
from pandas.io.json import json_normalize

path_list = glob.glob('./worklists/*.json')  # 讀取json檔案
df_all = pd.DataFrame()

def get_data() :
    for file in path_list :
        with open(file, 'r', encoding='utf-8') as load_f :
            # print(file)
            load_dict = json.load(load_f)
            # 讀取檔案名稱當作 key
            workid = re.sub('[^0-9]', '', file) #清除不為0-9的元素
            df = json_normalize(load_dict[workid],max_level=0)
            #將第一層的資料提取出來做為columns
            # columns = load_dict[workid].keys
            # print(columns)
            print(df)
            # df = pd.DataFrame.from_dict({(i, j):
            #                        load_dict[i][j]for i in load_dict.keys()
            #                        for j in load_dict[i].keys()},
            #                        orient='index').T
            # print(df)
            df.to_csv('./test.csv',index=False)
            time.sleep(30)
            # dict_df = pd.DataFrame([ast.literal_eval(i) for i in df.data.values])

get_data()

