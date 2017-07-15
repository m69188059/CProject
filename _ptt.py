import _ptool
import time

url='https://www.ptt.cc/bbs/Gossiping/index.html'
page = _ptool.get_web(url)
keyword = '賴清德'

r = 1
start=time.time()

while True:
    web = []
    print(r)
    r=r+1

    html=_ptool.get_doc(page)
    web = _ptool.get_articles(keyword,html)
    try:
      for match_article in web:
          article_push = []

          print(match_article['title'])     
          
          article_page = _ptool.get_web(match_article['link'])
          article_html = _ptool.get_doc(article_page)
          article_push = _ptool.get_push(article_html)
          context = _ptool.get_in_article(article_html)
         
          print(context)
          print("Link:")
          print(match_article['link'])
         
          print("推文數：")
          print(article_push[0]) 
          print("回文數：")
          print(article_push[1])
          print("噓文數：")
          print(article_push[2])
          
    except TypeError as e:
          pass 

    url = _ptool.get_back(html)
    if url is '1':
       break;
    page = _ptool.get_web(url)
        
tnd=time.time()
print(tnd-start)
