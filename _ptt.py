import _ptool
import time

page = _ptool.get_web_page('https://www.ptt.cc/bbs/Gossiping/index.html')

if page:
    date = time.strftime("%m/%d").lstrip('0')
    cu = _ptool.get_articles(page,date)
    for post in cu:
        print(post)
