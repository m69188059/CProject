import _ptool

url='https://www.ptt.cc/bbs/Gossiping/index100.html'
page = _ptool.get_web(url)
keyword = '八卦'
_isfirst = 1


while True:
    web = []
    if _isfirst:
       _isfirst = 0
    else:
       url = _ptool.get_back(page)
       if url is '1':
          break;
       page = _ptool.get_web(url)
    web = _ptool.get_articles(page,keyword)
    for post in web:
        print(post['title'])

