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


#mongodb
from pymongo import MongoClient
import dateutil
import dateutil.parser
client = MongoClient()
db = client.article_test


#initial set
#key = "%E5%90%8C%E5%A9%9A"

key = sys.argv[1]
filekey = key
key = quote(key, safe='/:?=&')
print(key)
num = sys.argv[2]
idx = '1'
website = 'https://www.ettoday.net/news_search/doSearch.php?keywords='+ key +'&idx='+ idx +'&page='
nowWeb = website + num

#nowWeb = sys.argv[1]
endpatt1 = '對此新聞評分：'
endpatt2 = '※你可能還想看：'

#印出網頁內容
print (nowWeb)
''' 
def getSearchPages(searchUrl):   
 page_html = urlopen(searchUrl)
 page_bsObj = BeautifulSoup(page_html,'lxml')
 result = page_bsObj.find("div", {"class":"pagination"},"ul").findAll("a",href=re.compile("^(http://www.cna.com.tw/search/)(.)*$"))
 return result
'''

def getLinks(articleUrl):   
 html = urlopen(articleUrl)
 bsObj = BeautifulSoup(html,'lxml')
 test = []
 print("---------------------------------")
 #print(bsObj)
 data = bsObj.find("div", {"id":"result-list"}).findAll('div',{'class':'box_1'})
 
 for div in data:
  links = div.findAll('a')
  for a in links:
   #print( a['href'])
   test.append(a['href']) 

 #print(test)
 return test
  
#searchlinks = getSearchPages(nowWeb)
#print("search links")
#print(searchlinks)
pages = set()
pages.add(nowWeb) 


while True:

 global pages
 #get new article
 
 links = getLinks(nowWeb)
 j=0
 
 for j in range(0,len(links),1):
  newArticle = links[j]
#.attrs["href"]	 
  print(newArticle)
  pages.add(newArticle)
 
  newpage = urlopen(newArticle)
  newpageSoup = BeautifulSoup(newpage,'lxml')
  #print(newpageSoup.h1.text) 
    
  arti_title = newpageSoup.h1.text 
  if arti_title in ['ETNEWS遊戲雲','房產雲','ETNEWS車雲',' ETNEWS 東森旅遊雲','ETNEWS星光雲']:
   continue
  print(arti_title)
  timetemp = newpageSoup.find('span', {'class':"news-time"})
  if timetemp is None:
   timetemp = newpageSoup.find('p',{'class':'date'})
  if timetemp is None:
   timetemp = newpageSoup.find('span',{'class':'date'})
  if timetemp is None:
   timetemp = newpageSoup.find('div',{'class':'date'})
   
  arti_time = timetemp.text
  #print('timetemp')
  #print(arti_time)

  
  arti_link = newArticle
  #print(arti_link)
 
  arti_text = newpageSoup.find('div',{'class':'story'})
  arti_text = arti_text.text
  #print(arti_text)
  #links = getLinks(nowWeb)
  
  post = {
  "_id" : arti_link,
  "time" : arti_time,
  "title" : arti_title,
  "context" : arti_text,
  "word" : "",
  "mood_score" : 0,
  "mood_update" : 0,
  "total" : 0
  }
   
  #insert to mongodb
  test = db.article_test
  find_or_not = test.find_one({"_id" : arti_link})
  if find_or_not is None:
   postid = test.insert_one(post).inserted_id 
  else:
   postid = test.update_one({"_id" : arti_link},{"$set" : post})
  print(postid) 
  print('okokokokokokok\n')
  
 #change new search page
 print(nowWeb)

 num = int(num) + 1
 if num > 1000:
  num = 1
  idx = int(idx) 
  idx = idx + 1
  idx = str(idx)

 num = str(num)
 newSearchPage = 'https://www.ettoday.net/news_search/doSearch.php?keywords='+ key +'&idx='+ idx +'&page='+ num
 print("*************************** next page *********************************")
 print(newSearchPage)
 
 if newSearchPage not in pages:
  pages.add(newSearchPage)
  nowWeb = newSearchPage

 else:
  print('url is existed')
  break
  

