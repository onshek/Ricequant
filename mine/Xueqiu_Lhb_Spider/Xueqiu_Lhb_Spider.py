__author__ = 'ipreacher'

import requests
import json
#import pprint
from pandas import DataFrame
s = requests.session()


headers = {'Referer': 'http://xueqiu.com/hq',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',
           'Host': 'xueqiu.com'
           }

url = 'http://xueqiu.com/hq'
s.get(url,headers=headers)

json_url = input('输入网址:\n')
# https://xueqiu.com/stock/f10/bizunittrdinfo.json?date=20170721&_=15
req = s.get(json_url,headers=headers)


#pprint.pprint(req.json())
data = req.json()
DataFrame = DataFrame(data['list'])
DataFrame_1 = DataFrame[['name', 'symbol']]
#print(DataFrame_1)
DataFrame_1.is_copy = False

for i in range(len(DataFrame.index)):
	for key in DataFrame.ix[i][2]:
		DataFrame_1.loc[i, 'tqQtBizunittrdinfo_' + key] = DataFrame.ix[i][2][key]
	for key in DataFrame.ix[i][3]:
		DataFrame_1.loc[i, 'tqQtSkdailyprice_' + key] = DataFrame.ix[i][3][key]	


print(DataFrame_1)

