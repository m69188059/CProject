import requests
from bs4 import BeautifulSoup

def get_web_page(url):
    resp = requests.get(
        url=url,
        cookies={'over18':'1'}
    )
    if resp.status_code !=200:
       print('Invalid url:',resp.url)
       return None
    else:
       return resp.text

def get_back(html):
    ptt = 'https://www.ptt.cc/'
    doc = BeautifulSoup(html,'html.parser')
    divs = doc.find_all('div','btn-group btn-group-paging')

    for d in divs:
            #if d.find('a','btn wide disabled') is not None:
              # if d.find('a','btn wide disabled').string=='‹ 上頁':
                 # ptt = 'https://www.ptt.cc/bbs/Gossiping/index1.html'
                  #break
               #else:
                  ptt= ptt+ d.find('a','btn wide',1,'‹ 上頁')['href']
       
    return ptt

def get_articles(html):
    soup = BeautifulSoup(html,'html.parser')
    
    articles = [] #save articles
    divs = soup.find_all('div','r-ent')
    for d in divs:
           push = 0 #push_count
           
           #get_push_count
           if d.find('div','nrec').string:
              try:
                  push = int(d.find('div','nrec').string)
              except ValueError:
                  pass
          
          #get_articles
           if d.find('a'):                #if article exists
              href = d.find('a')['href']
              title = d.find('a').string
              articles.append({
                   'title':title,
                   'href':href,
                   'push':push
              })
    return articles
