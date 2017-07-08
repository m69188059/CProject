import requests
import re
from bs4 import BeautifulSoup

def get_web(url):
    resp = requests.get( url=url, cookies={'over18':'1'})      #for 18 verification
    if resp.status_code !=200:
       print('Invalid url:',resp.url)
       return None
    else:
       return resp.text

def get_back(html):
    doc = BeautifulSoup(html,'html.parser')
    divs = doc.find_all('div','btn-group btn-group-paging')
    
    ptt_url = 'https://www.ptt.cc/'
    done = '0'
    for d in divs:
        if d.find('a','btn wide','1','‹ 上頁'):
           ptt_url= ptt_url+ d.find('a','btn wide',1,'‹ 上頁')['href']
        else:
           done = '1'
           break
    
    if done is '1':
         return done
    return ptt_url

def get_articles(html,search_key):
    doc = BeautifulSoup(html,'html.parser')
    divs = doc.find_all('div','r-ent')
    
    ptt = 'https://www.ptt.cc/'   
    articles = []                       
    pattern = search_key + '+'                       #set keyword

    for d in divs:
           push = 0                             
           
           #=== get_push_count ===


           if d.find('div','nrec').string:
              try:
                  push = int(d.find('div','nrec').string)
              except ValueError:
                  pass

          #=== get_articles ===
           if d.find('a'):                              #article exists
              title = d.find('a').string
              
              if re.findall(pattern,title):             #article matches keyword
                 href = d.find('a')['href']
                 articles.append({
                    'title':title,
                    'link':ptt+href,
                    'push':push })
    return articles

def get_in_article(html):
    soup = BeautifulSoup(html,'html.parser')
    divs = soup.find_all('div','article-metaline')
    #put time parameter
    #for d in divs:
        #print(d.find('span','article-meta-value',3))
