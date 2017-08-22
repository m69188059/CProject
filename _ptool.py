import requests
from bs4 import BeautifulSoup

def get_web(url):
    resp = requests.get( url=url, cookies={'over18':'1'}) 
    if resp.status_code !=200:
       print('Invalid url:',resp.url)
       return None
    else:
      # print (resp.text)
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
           if d.find('a'):                         #article exists
              title = d.find('a').string                  
            
              try:
                title.find(search_key)                
              except AttributeError as e:
                return None
              else:
                if title.find(search_key) is not -1:
                   href = d.find('a')['href']
                   author = d.find('div','author').string
                 
                   articles.append({
                       'title':title,
                       'link':ptt+href,
                       'author':author })
             
    return articles

def get_in_article(doc):

    _dict = {}

    spans = doc.find_all('span','article-meta-value')  
    timestr = ""
    try:
       timestr = timestr +spans[3].string +'\n'
    except IndexError as e:
       pass

    content = doc.find('div',id="main-container").getText()

    del_index=content.find('※ 發')
    content = content [1:del_index]
    del_index=content.find('\n')
    content = content[del_index:]

    _dict= {'time':timestr,'text':content}

    return _dict

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
def get_retext(doc):
    divs = doc.find_all('div','push')
    retext = []

    for d in divs:
        
        try:
           push = d.find('span','push-tag').string
        except AttributeError as e:
           push = ''
        
        try:
           userid = d.find('span','push-userid').string
        except AttributeError as e:
           userid =''
        
        try:
           content = d.find('span','push-content').string

           if content is None:
              content = content.find('a').string
        except AttributeError as e:
           content = ''
        
        try:
           retime = d.find('span','push-ipdatetime').string
        except AttributeError as e:
           retime = ''
        
        retext.append({
        'Pushtag':push,
        'Userid':userid,
        'Content':content,
        'Retime':retime })
     
    return retext
       


def get_index(doc):
    divs = doc.find('div','btn-group-paging').find_all('a','btn')
    link = divs[1].get('href')
    
    i_index = link.find('index') 
    e_index = link.find('.html')

    num = int(link[i_index+5:e_index])
    
    return num

def get_detail(title,timestr):
    data = {}

    time = timestr.split()
 
    isRe = 'False'
    if title[0]=='R'and title[1]=='e':
       isRe = 'True'
         
    kind = ''
    _get=0   
    if title.find('[') is not -1:   
       _get = title.find('[')+1
       try:
          kind = title[_get:_get+2]
       except IndexError as e:
          pass
    try:
      data = {
        'Week':time[0],
        'Month':time[1],
        'Date':time[2],
        'Time':time[3],
        'Year':time[4],
        'Isre':isRe,
        'Kind':kind}
    except IndexError as e:
      data = {
        'Week':"Error",
        'Month':"Error",
        'Date':"Error",
        'Time':"Error",
        'Year':"Error",
        'Isre':isRe,
        'Kind':kind}

    return data
