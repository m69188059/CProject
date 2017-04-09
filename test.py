#coding=utf-8

import requests
from bs4 import BeautifulSoup
import lxml

#GET<Response [200]>
res = requests.get("https://www.google.com.tw/search?client=ubuntu&channel=fs&q=%E6%9F%AF%E6%96%87%E5%93%B2&ie=utf-8&oe=utf-8&gfe_rd=cr&ei=P9TpWM3HKOCT9QX7nZDADQ")

#經過BeautifulSoup內lxml編輯器解析的結果
soup = BeautifulSoup(res.text,'lxml')

#印出網頁內容
#print soup 

#select
i=0
for i in range(0,100,1):
    title = soup.select('a')[i].text
    print title
    
for i in range(0,100,1):
    span = soup.select('span')[i].text
    print span




