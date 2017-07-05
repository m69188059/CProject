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

#initial set
key = "%E5%90%8C%E5%A9%9A"
nowWeb = '/search/hysearchws.aspx?q='+ key

#印出網頁內容
print (nowWeb)
 
def getSearchPages(searchUrl):   
 page_html = urlopen("http://www.cna.com.tw"+searchUrl)
 page_bsObj = BeautifulSoup(page_html,'lxml')
 #print(page_bsObj)
 return page_bsObj.find("div", {"class":"pagination"},"ul").findAll("a",href=re.compile("^(/search/)(.)*$"))



def getLinks(articleUrl):   
 html = urlopen("http://www.cna.com.tw"+articleUrl)
 bsObj = BeautifulSoup(html,'lxml')
 print("---------------------------------")
 return bsObj.find("div", {"class":"search_result_list"},"ul").findAll("a",href=re.compile("^(/news/)((?!:).)*$"))
  
searchlinks = getSearchPages(nowWeb)
print(searchlinks)
pages = set()
pages.add(nowWeb) 
searchIdx=0
for searchIdx in range(1,len(searchlinks)-1,1):
#while len(links) > 0:
 global pages
 #get new article
 
 links = getLinks(nowWeb)
 j=0
 for j in range(0,len(links)-1,1):
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
  links = getLinks(nowWeb)
 
 #change new search page
 newSearchPage = searchlinks[searchIdx].attrs["href"]
 print("*************************** next page *********************************")
 print(newSearchPage)
 pages.add(newSearchPage)
 
 newSearchPage_html = urlopen("http://www.cna.com.tw"+newSearchPage)
 newSearchPage_Soup = BeautifulSoup(newSearchPage_html,'lxml')
 nowWeb = newSearchPage
 
 
 #print(links)





