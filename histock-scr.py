import pandas as pd
import numpy as np
from requests_html import HTMLSession

ss = HTMLSession()

Money = 1000000

df = pd.read_html('https://histock.tw/stock/taiexproportion.aspx')
df = pd.DataFrame(df[0])
# column title 等於 0, 1, 2, 3 才用
df.columns = np.array(df[:1])[0]
df = df.drop([0])
# ^^^^^
MarketValue = np.array(df[:50]['市值佔大盤比重'].str.rstrip('%').astype('float')) / 100
SumValue = np.sum(MarketValue)
AdjustValue = 1 / SumValue
A = MarketValue * AdjustValue
F = np.array(df[:50]['名稱'])
B = A * Money
C = np.array(df[:50]['代號'].astype('str'))
stockUrl = 'https://histock.tw/stock/'
E, D = [], []
# 輸出沒有要用 dataframe 可以不用
name = ["{}-{}".format(C[i], item) for i, item in enumerate(F)]
columns = ["股票代號", "股價", "購買股數", "投資金額"]
# ^^^^
for i in range(0, 50):
    res = float(ss.get(stockUrl + C[i]).html.find("span#Price1_lbTPrice")[0].text)
    E.append(res)
    D.append(round(B[i] / E[i], 0))
    # print("{}.\t股票代號: {}-{},\t股價: {},\t購買股數: {},\t投資金額: {}".format(i+1, C[i], F[i], E[i], D[i], round(B[i], 0) ))

# 輸出沒有要用 dataframe 可以不用
res_df = pd.DataFrame(np.array(np.transpose([name, E, D, np.round(B, 0)])), columns=columns)
res_df.index += 1
print(res_df)