import _ptool
import time

url='https://www.ptt.cc/bbs/Gossiping/index.html'
page = _ptool.get_web(url)
keyword = '新聞'
_isfirst = 1

#r = 1
#start=time.time()

while True:
    web = []

 #   print(r)
 #   r=r+1

    html=_ptool.get_doc(page)
    
    if _isfirst:
       _isfirst = 0
    else:
       url = _ptool.get_back(html)
       if url is '1':
          break;
       page = _ptool.get_web(url)

    web = _ptool.get_articles(keyword,html)
    try:
        for post in web:
          #  print(post['title'])
            page_1 =  _ptool.get_web(post['link'])
            html_1 = _ptool.get_doc(page_1)
            _ptool.get_in_article(html_1)
            print(post['link'])
    except TypeError as e:
        pass
   
        
#tnd=time.time()
#print(tnd-start)
