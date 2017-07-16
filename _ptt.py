import _ptool
import sys
import time
from io import open

url='https://www.ptt.cc/bbs/Gossiping/index.html'
page = _ptool.get_web(url)
keyword = sys.argv[1]

r = 1
num = 0
start=time.time()

print("Keyword is:")
print(sys.argv[1])
print("Start!")
print("=================================================================")

while True:
    web = []
    print(r)
    r=r+1

    html=_ptool.get_doc(page)
    web = _ptool.get_articles(keyword,html)
    try:
      for match_article in web:
          article_push = []
        
          file_name = str(num)+ "_"+ keyword + "_" +str(r) + ".txt"
          num = num + 1

          with open(file_name,mode = 'w',encoding='utf8') as fin:
             fin.write(match_article['title'])     
          
             article_page = _ptool.get_web(match_article['link'])
             article_html = _ptool.get_doc(article_page)
             article_push = _ptool.get_push(article_html)
             context = _ptool.get_in_article(article_html)
         
             fin.write(context)
             fin.write("Link:")
             fin.write(match_article['link'])
         
             fin.write("\n推文數：")
             fin.write(str(article_push[0])) 
             fin.write("\n回文數：")
             fin.write(str(article_push[1]))
             fin.write("\n噓文數：")
             fin.write(str(article_push[2]))
             fin.close()
             print(fin.closed)  #check_file_closed
    except TypeError as e:
          pass 

    url = _ptool.get_back(html)
    if url is '1':
       break;
    page = _ptool.get_web(url)
        
tnd=time.time()
print(tnd-start)
