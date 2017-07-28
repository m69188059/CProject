import _ptool
import sys
import time
import random
from io import open
from threading import Thread, Lock

url='https://www.ptt.cc/bbs/Gossiping/index.html'
pagefornum = _ptool.get_web(url)
docfornum = _ptool.get_doc(pagefornum)

num = _ptool.get_index(docfornum) + 1
data_n = 1
print('home page is :%d'%(num))
print('====================================================================')

def mul_ptt(tid,keyword,lock):
    while True:

      with lock:
           global num
           if num>0:              
     
              ptt_url = 'https://www.ptt.cc/bbs/Gossiping/index' + str(num) + '.html'          
              page_num = num
              num = num - 1           

              print('thread id %d at link : %s'%(tid,ptt_url))

              web = []            
              page = _ptool.get_web(ptt_url)
              html = _ptool.get_doc(page)
              web = _ptool.get_articles(keyword,html)                                 #find the all articles that match keyword
              
              
              try:
                for match_article in web:
                    article_push = []
                    
                    global data_n                                     
                    file_name = str(data_n)+ "_"+ keyword  + '_' + str(tid)+ ".txt"           #global
                    data_n = data_n + 1
                   
                   
              
                   
                    with open(file_name,mode = 'w',encoding='utf8') as fin:
                      
                      
                        # print('thread id %d is writing data in page %d' %(tid,page_num))

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
                         print('thread id %d closed status :'%(tid))
                         print(fin.closed)  #check_file_closed

              except TypeError as e:
                   pass
                        
           elif num==0:
                print("done")
                break
       



kword = sys.argv[1]

for i in range(10):
    t = Thread(target=mul_ptt, args=(i,kword,Lock()))
    t.start()
