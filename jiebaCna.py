#encoding=utf-8
import jieba
import jieba.posseg as pseg

jieba.set_dictionary('./jieba/extra_dict/dict.txt.big')
#jieba.set_dictionary('./jieba/test/TestCna.txt')
#jieba.set_dictionary('./jieba/extra_dict/homo.txt')
jieba.load_userdict("./jieba/test/userdict.txt")

'''
jieba.suggest_freq(('跨性戀'), True)
jieba.suggest_freq(('同性伴侶'), True)
jieba.add_word(('跨性戀'), None, 'n')
jieba.add_word(('同性伴侶'), None, 'n')
jieba.add_word(('蔡英文'), None, 'n')
jieba.add_word(('恐同日'), None, 'n')
jieba.add_word(('蔡總統'), None, 'n')
jieba.add_word(('彩虹卡'), None, 'n')
jieba.add_word(('林奕含'), None, 'n')
'''

#content = open('SearchOutputCna.txt', 'rb').read()
content = open('test1.txt', 'rb').read()

#print (content)

#words = jieba.cut(content, cut_all=False)
words = pseg.cut(content)
#print ("Output 精確模式 Full Mode：")
for word, flag in words:
    print('%s %s' % (word, flag))
