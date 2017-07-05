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

def get_articles(html,date):
    soup = BeautifulSoup(html,'html.parser')
    
    articles = [] #save articles
    divs = soup.find_all('div','r-ent')
    for d in divs:
        #if d.find('div','date').string == date:
          #push_count
           push = 0
           if d.find('div','nrec').string:
              try:
                  push = int(d.find('div','nrec').string)
              except ValueError:
                  pass
          
          #get
           if d.find('a'):
              href = d.find('a')['href']
              title = d.find('a').string
              articles.append({
                  'title':title,
                  'href':href,
                  'push':push
              })
    return articles
