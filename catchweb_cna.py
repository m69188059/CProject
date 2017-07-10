#coding=utf-8

import requests
from bs4 import BeautifulSoup
import lxml

#輸出txt檔要指定utf-8
#import imp
#imp.reload(sys)
#sys.setdefaultencoding('utf-8')

from urllib.request import urlopen
from urllib.parse import quote
import datetime
import re
import sys

#initial set
#key = "%E5%90%8C%E5%A9%9A"
key = sys.argv[1]
key = quote(key, safe='/:?=&')
print(key)
nowWeb = 'http://www.cna.com.tw/search/hysearchws.aspx?q='+ key

#印出網頁內容
print (nowWeb)
 
def getSearchPages(searchUrl):   
 page_html = urlopen(searchUrl)
 page_bsObj = BeautifulSoup(page_html,'lxml')
 result = page_bsObj.find("div", {"class":"pagination"},"ul").findAll("a",href=re.compile("^(http://www.cna.com.tw/search/)(.)*$"))
 return result


def getLinks(articleUrl):   
 html = urlopen(articleUrl)
 bsObj = BeautifulSoup(html,'lxml')
 print("---------------------------------")
 #print(bsObj)
 return bsObj.find("div", {"class":"search_result_list"},"ul").findAll("a",href=re.compile("^(/news/)((?!:).)*$"))
  
#searchlinks = getSearchPages(nowWeb)
#print("search links")
#print(searchlinks)
pages = set()
pages.add(nowWeb) 
searchIdx=1

while True:

 global pages
 #get new article

 links = getLinks(nowWeb)
 j=0
  
 for j in range(0,len(links),1):
  newArticle = links[j].attrs["href"]	 
  print(newArticle)
  pages.add(newArticle)
 
  newpage = urlopen("http://www.cna.com.tw"+newArticle)
  newpageSoup = BeautifulSoup(newpage,'lxml')
  print(newpageSoup.h1.text)
  timetemp = newpageSoup.find(attrs = {'class':"update_times"})
  timetemp = newpageSoup.find(attrs = {'class':'blue'}) 
  print(timetemp.text)
  
  i=0
  for i in range(3,7,1):
   context = newpageSoup.select('p')[i].text
   print(context)
  links = getLinks(nowWeb)
  
 #change new search page
 if searchIdx == 1: #p1 -> p11 search only at first page
  searchlinks = getSearchPages(nowWeb)
 if searchlinks == -1:
  break
 print(nowWeb)
 newSearchPage = searchlinks[searchIdx].attrs["href"]
 #print("*************************** next page *********************************")
 print(newSearchPage)
 
 
  
 #change chinese to url
 newSearchPage = quote(newSearchPage, safe='/:?=&')
 print(newSearchPage) 
 newSearchPage_html = urlopen(newSearchPage)
 newSearchPage_Soup = BeautifulSoup(newSearchPage_html,'lxml')
 nowWeb = newSearchPage
 print(nowWeb)
 
 if newSearchPage not in pages:
  pages.add(newSearchPage)
  searchIdx =searchIdx + 1

 else:
  break
  
 if searchIdx >= len(searchlinks):
  searchlinks = getSearchPages(nowWeb)
  searchIdx = 2
  print(searchIdx)

 
#print(links)
