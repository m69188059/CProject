import requests
from bs4 import BeautifulSoup

def get_web(url):
    resp = requests.get( url=url, cookies={'over18':'1'}) 
    if resp.status_code !=200:
       print('Invalid url:',resp.url)
       return None
    else:
       return resp.text

def get_doc(page):
    page = BeautifulSoup(page,'html.parser')
    return page

def get_back(doc):
    divs = doc.find('div','btn-group-paging').find_all('a','btn')
    link = divs[1].get('href')
    if link is None:
       return '1'
    else:
       ptt_url = 'https://www.ptt.cc' + link
       return ptt_url

def get_articles(search_key,doc):
    divs = doc.find_all('div','r-ent')   
    ptt = 'https://www.ptt.cc'   
    articles = []                       
    
    for d in divs:
           push = ''   
           if d.find('div','nrec').string:
              push = d.find('div','nrec').string

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
    spans = doc.find_all('span','article-meta-value')  
    timestr = "\nTime: "
    try:
       timestr = timestr +spans[3].string + '\n\n' #get article time
    except IndexError as e:
       pass

    content = doc.find('div',id="main-container").getText()
    del_index=content.find('--')
    content = content [1:del_index]
    del_index=content.find('\n')
    content = content[del_index:]
    content = content + timestr
    return content

def get_push(doc):
    spans = doc.find_all('span','push-tag')
    push = [0,0,0]
     
    for s in spans:
        tem = s.string
        if tem.find('推') is not -1:
           push[0]=push[0]+1
        elif tem.find('→ ') is not -1:
           push[1]=push[1]+1
        elif tem.find('噓') is not -1:
           push[2]=push[2]+1
    
    return push

def get_index(doc):
    divs = doc.find('div','btn-group-paging').find_all('a','btn')
    link = divs[1].get('href')
     
    end_index = link.find('.html') 

    num = int(link[20:end_index])
    return num

