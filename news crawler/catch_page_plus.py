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
website = 'http://www.cna.com.tw/search/hysearchws.aspx?q='+ key + '&p=' 
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
 print("---------------------------------")
 #print(bsObj)
 return bsObj.find("div", {"class":"search_result_list"},"ul").findAll("a",href=re.compile("^(/news/)((?!:).)*$"))
  
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
  newArticle = links[j].attrs["href"]	 
  print(newArticle)
  pages.add(newArticle)
 
  newpage = urlopen("http://www.cna.com.tw"+newArticle)
  newpageSoup = BeautifulSoup(newpage,'lxml')
  print(newpageSoup.h1.text) 
    
  arti_title = newpageSoup.h1.text 
  
  timetemp = newpageSoup.find(attrs = {'class':"update_times"})
  timetemp = newpageSoup.find(attrs = {'class':'blue'}) 
  
  i=0
  arti_link = 'http://www.cna.com.tw'+newArticle
  filelink = newArticle.replace('/','_')
  filename = 'http:__www.cna.com.tw'+filelink+'.txt'
  fileloc = "/home/brendatsai011220/crawler/txt/"+filename
  
  f = open(fileloc, 'w', encoding = 'UTF-8') 
  f.write(arti_title+'\n')
  
  arti_time = timetemp.text
  delete = re.search("(最新更新：)",arti_time)
  arti_time = arti_time[delete.end():]
  myDatetime = dateutil.parser.parse(arti_time)  
  f.write(arti_time+'\n')
  
  arti_text = ''
  for i in range(3,20,1):
   context = newpageSoup.select('p')[i].text    
   if(context == endpatt1):
    i=21
    break
   if(endpatt2 in context):
    delete = re.search("(※你可能還想看：)",context)
    context = context[:delete.start()]
   arti_text = arti_text + context 	
   f.write(context)
  f.close() 
  links = getLinks(nowWeb)
  
  post = {
  "_id" : arti_link,
  "time" : arti_time,
  "title" : arti_title,
  "context" : arti_text,
  "word" : "",
  "mood_update" : 0,
  "mood_score" : 0,
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
 num = str(num)
 newSearchPage = website + num
 print("*************************** next page *********************************")
 print(newSearchPage)
 
 if newSearchPage not in pages:
  pages.add(newSearchPage)
  nowWeb = newSearchPage

 else:
  print('url is existed')
  break
  
 
