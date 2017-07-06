import _ptool

url='https://www.ptt.cc/bbs/Gossiping/index.html'
page = _ptool.get_web_page(url)

for x in range(0,5):
    cu = []
    if x == 0 :
       cu = _ptool.get_articles(page)
   
    else:
       url = _ptool.get_back(page)
       page =_ptool.get_web_page(url)
       cu = _ptool.get_articles(page)

    for post in cu:
         print(post)
