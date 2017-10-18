import requests
from bs4 import BeautifulSoup

def get_web(url):
    resp = requests.get( url=url, verify = True ,cookies={'over18':'1'}) 
    if resp.status_code !=200:
       print('Invalid url:',resp.url)
       return None
    else:
      # print (resp.text)
       return resp.text

def get_doc(page):
    try:
        page = BeautifulSoup(page,'html.parser')
        return page
    except TypeError as e:
        print("TyepError, getting error link")
        return False

def get_articles(doc):
    try:
           divs = doc.find_all('div','r-ent')
    except AttributeError as e:
           print("AttributeError, getting error link")
           return False 

  
    ptt = 'https://www.ptt.cc'   
    articles = []                       
    
    for d in divs:
           if d.find('a'):                         #article exists
              title = d.find('a').string              
              href = d.find('a')['href']
              author = d.find('div','author').string
			  date = d.find('div','date').string
              
			  articles.append({
                'title':title,
                'link':ptt+href,
                'author':author,
			    'date':date})
             
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
    re = '\n'

    for d in divs:
        
        try:
           push = d.find('span','push-tag').string
        except AttributeError as e:
           push = '='
        
        try:
           userid = d.find('span','push-userid').string
        except AttributeError as e:
           userid ='=userid'
        
        try:
           content = d.find('span','push-content').string

           if content is None:
              content = content.find('a').string
        except AttributeError as e:
           content = '====URL is here!!!!===='
        
        try:
           retime = d.find('span','push-ipdatetime').string
        except AttributeError as e:
           retime = '==='
        
        re = re + push + ' ' + userid + ' ' + content + ' ' + retime + '\n'
        
     
    return re
       
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
        'Year':time[4],
        'Isre':isRe,
        'Kind':kind}
    except IndexError as e:
      data = {
        'Year':"Error",
        'Isre':isRe,
        'Kind':kind}

    return data
