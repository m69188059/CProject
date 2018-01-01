"""
reference: http://www.jianshu.com/p/4cfcf1610a73
"""


"""
senLoc = list(senWord.keys())
若沒有list則會出現TypeError: 'dict_keys' object does not support indexing
def Dic(Word):
轉換成Dic[word]= 0(1,2,3 ...)
"""






from collections import defaultdict
import os
import re
import jieba
import codecs
"""
1. 文本切割
"""
def sent2word(sentence):
    #print (sentence)
    """
    Segment a sentence to words
    Delete stopwords
    """
    segList = jieba.cut(sentence)
    segResult = []
    for w in segList:
        segResult.append(w)
    
    #stopwords = readLines('stop_words.txt')
    fo= open('stop_words.txt', 'r+')
    stopwords= fo.readlines()
    newSent = []
    for word in segResult:
        if word in stopwords:  #print ("stopword: %s" % word)
            continue
        else: newSent.append(word)
    fo.close()    
    return newSent
    
    #return segResult
"""
2. 情感定位
"""
def classifyWords(wordDict):
    #print (wordDict.keys())
    # (1) 情感词
    fo= open('2_BosonNLP_sentiment_score.txt', 'r',encoding = 'UTF-8')#('2_BosonNLP_sentiment_score.txt', 'r',encoding = 'UTF-8')
    #fo= u.fo.encode('utf-8')
    sendList= fo.readlines()
    #print(sendList)
    #print(sendList)
    #senList = readline('BosonNLP_sentiment_score.txt')#readLines('BosonNLP_sentiment_score.txt')
    senDict = defaultdict()
    #print(sendList)
    #while True:
    fo.close()
    for s in sendList:
        senDict[s.split(' ')[0]] = s.split(' ')[1]
        #print (s.split(' ')[1])
    #print ("SendList")
    #print (senDict.keys())
    
    # (2) 否定词
    fo= open('notDict_tra.txt', 'r', encoding= 'UTF-8')
    notList= fo.readline()
    fo.close()
    #notList = readLines('notDict.txt')
    
    # (3) 程度副词
    fo= open('DEGREE.txt', 'r+')#('degreeDict_tra.txt', 'r+')
    degreeList= fo.readlines()
    fo.close()
    #degreeList = readLines('degreeDict.txt')
    degreeDict = defaultdict()
    #print(degreeList)
    for d in degreeList:
        degreeDict[d.split(',')[0]] = d.split(',')[1]
    
    senWord = defaultdict()
    notWord = defaultdict()
    degreeWord = defaultdict()
    """
    for word in wordDict:#.keys():
        if word in senDict.keys() and word not in notList and word not in degreeDict.keys():
            #senWord[wordDict[word]] = senDict[word]
            senWord[word] = senDict[word]
        elif word in notList and word not in degreeDict.keys():
            #notWord[wordDict[word]] = -1
            notWord[word] = -1
        elif word in degreeDict.keys():
            #degreeWord[wordDict[word]] = degreeDict[word]
            degreeWord[word] = degreeDict[word]
    
    """
    #for word in wordDict.keys():
        #print (word)
    """
    for word in wordDict.keys():
        if word in senDict.keys() and word not in notList and word not in degreeDict.keys():
            senWord[wordDict[word]] = senDict[word]
        elif word in notList and word not in degreeDict.keys():
            notWord[wordDict[word]] = -1
        elif word in degreeDict.keys():
            degreeWord[wordDict[word]] = degreeDict[word]
    """
    """
    #print (len(wordDict))
    for num in range(0, Len):
        for word in wordDict.keys():
            if wordDict[word] is num:
                if word in senDict.keys() and word not in notList and word not in degreeDict.keys():
                    senWord[wordDict[word]] = senDict[word]
                elif word in notList and word not in degreeDict.keys():
                    notWord[wordDict[word]] = -1
                elif word in degreeDict.keys():
                    degreeWord[wordDict[word]] = degreeDict[word]
    """
    for word in wordDict.keys():
        if word in senDict.keys() and word not in notList and word not in degreeDict.keys():
            senWord[wordDict[word]] = senDict[word]
        elif word in notList and word not in degreeDict.keys():
            notWord[wordDict[word]] = -1
        elif word in degreeDict.keys():
            degreeWord[wordDict[word]] = degreeDict[word]
    
    #print (senWord, notWord, degreeWord)
    return senWord, notWord, degreeWord

"""
3. 情感聚合
"""
def scoreSent(senWord, notWord, degreeWord, segResult):
    W = 1
    score = 0 # 存所有情感词的位置的列表
    senLoc = list(senWord.keys())
    #print ('senLoc')
    #print (senLoc)
    notLoc = list(notWord.keys())
    #print (notLoc)
    degreeLoc = list(degreeWord.keys())
    #print (degreeLoc)
    senloc = -1
    # notloc = -1
    # degreeloc = -1
    
    """
    print ("degreeWord.keys")
    print (degreeWord.keys())
    
    print ("printttttt")
    print (degreeLoc)
    
    print (segResult)
    print (len(segResult))
    """
    """
    print ("================================")
    print (senLoc[0])
    print (len(senLoc))
    print (senWord[1])
    """
    #print (len(segResult))
    # 遍历句中所有单词segResult，i为单词绝对位置
    for i in range(0, len(segResult)):
        # 如果该词为情感词
        if i in senLoc:
            # loc为情感词位置列表的序号
            senloc += 1
            # 直接添加该情感词分数
            score += W * float(senWord[i])
            #print ("score = %f"  % score)
        
            if senloc < len(senLoc) - 1:
                # 判断该情感词与下一情感词之间是否有否定词或程度副词
                # j为绝对位置
                for j in range(senLoc[senloc], senLoc[senloc]+ 1): #senLoc[senloc +1]
                    #print (senLoc[senloc], senLoc[senloc]+ 1)
                    # 如果有否定词
                    if j in notLoc:
                        W *= -1
                    # 如果有程度副词
                    elif j in degreeLoc:
                        #print情 (j)
                        W *= float(degreeWord[j])
                        #print ('W')
                        #print (W)
                
        # i定位至下一个情感词
        if senloc < len(senLoc) - 1:
            i = senLoc[senloc + 1]    
    return score

def Dic(Word):
    WordDict = defaultdict()
    i= 0
    #print (Word[1])
    for w in Word:
        #print (w, i)
        WordDict[w] = i
        i= i+1
    #print (WordDict['尼玛'])
    return WordDict

#fo = open('senTest.txt', 'r')
#content= fo.readline()
#fo.close()
"""
mongoDB
"""

from pymongo import MongoClient
client = MongoClient()
db= client['ptt']
collect= db['Gossiping2']
"""
db= client['senti_Test']
collect= db['Test']
"""

for post in collect.find({"Negative": 0}):
    ids= post['_id']
    retext= post['Retext']
    test_retext= sent2word(retext)
    test_retext= Dic(test_retext)
    (test1, test2, test3) =classifyWords(test_retext)
    score1= scoreSent(test1, test2, test3, test_retext)

    text= post['Text']
    test_text= sent2word(text)
    test_text= Dic(test_text)
    (test1, test2, test3) =classifyWords(test_text)
    score2= scoreSent(test1, test2, test3, test_text)

    score= score1+ score2
    
    post['Negative']= -1
    post['Score']= score
    collect.update_one({'_id': ids}, {'$set': post})
    print(score)


"""
for post in collect.find({"mood_update": 0}):
    #print(post)
    document = dict(post)
    test= document['context']
    test= sent2word(test)
    test= Dic(test)
    (test1, test2, test3) =classifyWords(test)
    print (scoreSent(test1, test2, test3, test))
    #print(test)
    #print(document['content'])
"""                          
#print (content)
#test= sent2word('有车一族都用了这个宝贝，后果很严重哦[偷笑][偷笑][偷笑]')


#test= sent2word(test)


#test= sent2word('有车一族都用了这个宝贝，后果很严重哦[偷笑][偷笑][偷笑]路痴不再迷路，省油[悠闲][悠闲][悠闲]5，保险公司裁员2成，s')
#省油[悠闲][悠闲][悠闲]5，保险公司裁员2成，保费折上折2成，全国通用[憨笑][憨笑][憨笑]买不买你自己看着办吧[调皮][调皮][调皮]2980元轩辕魔镜带回家，推广还有返利[得意]')
#Len= len(test)
#print (len('有车一族都用了这个宝贝，后果很严重哦[偷笑][偷笑][偷笑]路痴不再迷路，省油[悠闲][悠闲][悠闲]5，保险公司裁员2成，s'))
#print (test)


#test= Dic(test)


#test= sorted(test.items(), key=lambda d:d[1], reverse = True)
#test= sorted(test)
#print (test)
#print (sent2word('有车一族都用了这个宝贝，后果很严重哦[偷笑][偷笑][偷笑]'))
#print (test)


#(test1, test2, test3) =classifyWords(test)


#print (test1, test2, test3)
#print (test1)
#print (classifyWords(test))
#print(scoreSent(test1, test2, test3, test))


#print (scoreSent(test1, test2, test3, test))
