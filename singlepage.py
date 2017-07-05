#coding=utf-8

import requests
from bs4 import BeautifulSoup
import lxml

#輸出txt檔要指定utf-8
#import imp
#imp.reload(sys)
#sys.setdefaultencoding('utf-8')

from urllib.request import urlopen
import datetime
import re

#GET<Response [200]>
res = requests.get("http://www.cna.com.tw/search/hysearchws.aspx?q=%E5%90%8C%E5%A9%9A")

#經過BeautifulSoup內lxml編輯器解析的結果
soup = BeautifulSoup(res.text,'lxml')

#印出網頁內容
#print soup 
def getLinks(articleUrl):   
 html = urlopen("http://www.cna.com.tw"+articleUrl)
 bsObj = BeautifulSoup(html,'lxml')
 print("---------------------------------")
 return bsObj.find("div", {"class":"search_result_list"},"ul").findAll("a",href=re.compile("^(/news/)((?!:).)*$"))
 
links = getLinks("/search/hysearchws.aspx?q=%E5%90%8C%E5%A9%9A")
#print("可惡")
pages = set() 
j=0
for j in range(0,len(links)-1,1):
#while len(links) > 0:
 global pages
 newArticle = links[j].attrs["href"]	 
 print(newArticle)
 pages.add(newArticle)
 
 newpage = urlopen("http://www.cna.com.tw"+newArticle)
 newpageSoup = BeautifulSoup(newpage,'lxml')
 print(newpageSoup.h1.text) 
 i=0
 for i in range(3,7,1):
  context = newpageSoup.select('p')[i].text
  print(context)
 links = getLinks("/search/hysearchws.aspx?q=%E5%90%8C%E5%A9%9A")
 #print(links)

#select
'''i=0
for i in range(0,1000,1):
    title = soup.select('h2')[i].text
    print(title)'''



