#encoding=utf-8
import numpy
from jieba import posseg

class IndexRule():
   
    def __init__(self, vocabulary ,sen_len=50, rule_path=None,flag=None):
        '''

        Params
        ------------
        rule_path: path of rule
        vocabulary: dict. str(word):int(index) 词典是模型的首要核心。
        flag: dict. str(word):str(flag) 需要人工对词性进行纠正。

        '''
        self.vocabulary=vocabulary
        self.rules=self.read_rules(rule_path) if rule_path!=None else []
        self.index2word=vocabulary.words
        self.index2flag={index:vocabulary.attr['flag'][word] for index,word in enumerate(vocabulary.words)}
        self.sen_len=sen_len


    def transform(self,indexs):
        mul=numpy.ones(self.sen_len)
        for i,w in enumerate(indexs):
            if w==-1:
                mul[i]*=0
                continue
            for rule in self.rules:
                if rule['type']=='cw':#单名单,作用域:本身加权
                    if self.index2word[w] in rule['key']:
                        mul[i]*=rule['ratio']
                
                if rule['type']=='cf':
                    if self.index2flag[w] in rule['key']:#匹配词性 作用域：本身加权
                        mul[i]*=rule['ratio']
                
                if rule['type']=='cw_nw':#匹配单词 作用域：本身变为0，下一个形容词加权乘
                    if self.index2word[w] in rule['key']:
                        k=self.find_next_word(indexs,i,rule['next'])
                        if k!=-1:
                            mul[i]*=0
                            mul[k]*=rule['ratio']
                        else:
                            mul[i]=0
                
                if rule['type']=='cw_ns':#匹配单词 作用域：本身变为0，下一短句加权乘
                    if self.index2word[w] in rule['key']:
                        l,r=self.find_next_sen(indexs,i)
                        mul[i]*=0
                        if l<len(indexs):
                            mul[l:r]*=rule['ratio']
        return mul

    def read_rules(self,rule_path):
        fp=open(rule_path,'r')
        rules=[]
        while True:
            rule={}
            while True:
                s=fp.readline().strip()
                if s=='':
                    break
                s=s.split('=')
                rule[s[0].strip()]=eval(s[1].strip())
            if rule=={}:
                break
            rules.append(rule)
        return rules

    def find_next_word(self, words, index, tarList):
        for i in range(index + 1, len(words)):
            if self.index2flag[words[i]] in tarList:
                return i
        return -1

    def find_next_sen(self, words, index):
        '''
        从第一个非标点符号开始，
        到下一个一个标点符号为止。标点符号为分句符号：逗号，句号。
        由于简陋，只能这样了。
        '''
        fuhao=['，','。','！','？']
        l=index+1
        if l<len(words):
            while self.index2word[words[l]] in fuhao:
                l+=1
                if l>=len(words):
                    break
        r=l
        if r<len(words):
            while self.index2word[words[r]] not in fuhao:
                r+=1
                if r>=len(words):
                    break

        return l,r

    def change():
        '''
        用index2word与index2flag确实挺慢的，逻辑不交清晰
        另一种方法是首先生成words的rules.然后利用iindex2word与index2flag将rules映射到index相关，那就不错了。
        只能将word隐射到index,原本的词性匹配现在还是要的。
        '''
        pass
        

