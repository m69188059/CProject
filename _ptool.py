import requests
from bs4 import BeautifulSoup

def get_web(url):
    resp = requests.get( url=url, cookies={'over18':'1'})      #for 18 verification
    if resp.status_code !=200:
       print('Invalid url:',resp.url)
       return None
    else:
       return resp.text

def get_doc(page):
    page = BeautifulSoup(page,'html.parser')
    return page

def get_back(doc):
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

def get_articles(search_key,doc):
    divs = doc.find_all('div','r-ent')
    
    ptt = 'https://www.ptt.cc/'   
    articles = []                       
    
    for d in divs:
           push = 0                             
           
           #=== get_push_count ===


           if d.find('div','nrec').string:
              try:
                  push = int(d.find('div','nrec').string)
              except ValueError:
                  pass

          #=== get_articles ===
           if d.find('a'):                         #article exists
              title = d.find('a').string                  
            
              try:
                title.find(search_key)                
              except AttributeError as e:
                return None
              else:
                if title.find(search_key) is not -1:
                   href = d.find('a')['href']
                   articles.append({
                       'title':title,
                       'link':ptt+href,
                       'push':push })
             
    return articles

def get_in_article(doc):
    divs = doc.find_all('div','article-metaline')
    
    for d in divs:
        st = d.find('span','article-meta-tag').string + ':' + d.find('span','article-meta-value').string
        print(st)
       
