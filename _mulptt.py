import _ptool
import sys
import os
from threading import Thread, Lock

ptt_name = sys.argv[3]

url = 'https://www.ptt.cc/bbs/' + ptt_name + '/index.html'
pagefornum = _ptool.get_web(url)
docfornum = _ptool.get_doc(pagefornum)

num = _ptool.get_index(docfornum) + 1
data_n = 1
print('home page is :%d'%(num))
print('home url is : %s'%(url))
print('====================================================================')

def mul_ptt(tid,keyword,lock,dir_path):
    while True:

      with lock:
           global num
           if num>0:              
              global ptt_name
              ptt_url = 'https://www.ptt.cc/bbs/' + sys.argv[3] + '/index' + str(num) + '.html'          
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
                    file_name = dir_path +"/" + str(data_n)+ "_"+ keyword + "_"+ str(tid) + ".txt"           #global
                    data_n = data_n + 1
                   
                   
              
                   
                    with open(file_name,mode = 'w',encoding='utf8') as fin:
                      
                         fin.write(match_article['title'])
                        
                         article_page = _ptool.get_web(match_article['link'])
                         article_html = _ptool.get_doc(article_page)
                        
                         article_push = _ptool.get_push(article_html)
                         retext = _ptool.get_retext(article_html)

                         _dict = _ptool.get_in_article(article_html)
                        
                         
                         _detail =  _ptool.get_detail(match_article['title'],_dict['time'])

                         fin.write(_dict['text'])
                         fin.write("\n\n")
                        
                                                 
                         fin.write("\nLink:")
                         fin.write(match_article['link'])
                         fin.write("\n\nAuthor: %s"%match_article['author'])

                         fin.write("\n\n推文數：")
                         fin.write(str(article_push[0]))
                         fin.write("\n回文數：")
                         fin.write(str(article_push[1]))
                         fin.write("\n噓文數：")
                         fin.write(str(article_push[2]))

                         fin.write("\n")
                         fin.write(_detail['Week'])
                         fin.write("\n")
                         fin.write(_detail['Month'])
                         fin.write("\n")
                         fin.write(_detail['Date'])
                         fin.write("\n")
                         fin.write(_detail['Time'])
                         fin.write("\n")
                         fin.write(_detail['Year'])
                         fin.write("\n")
                         fin.write(_detail['Isre'])
                         fin.write("\n")
                         fin.write(_detail['Kind'])


                         fin.write(retext)
                         fin.close()
                         print('thread id %d closed status :'%(tid))
                         print(fin.closed)  #check_file_closed

              except TypeError as e:
                   pass
                        
           elif num==0:
                print("done")
                break
       


tnum = int(sys.argv[2])
kword = sys.argv[1]
dir_name = sys.argv[3]+ '_' +kword


if tnum is 0:
   tnum = 10 #defult thread_num

if not os.path.exists(dir_name):
   os.makedirs(dir_name)


for i in range(tnum):
    t = Thread(target=mul_ptt, args=(i,kword,Lock(),dir_name))
    t.start()
