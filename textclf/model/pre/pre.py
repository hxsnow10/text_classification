# -*- coding: utf8
import re
from textclf.util.pick import *
import jieba
import os
import sys
import datetime
from textclf.vocab.words import Vocabulary
from functools import partial

class Preprocess:
    def __init__(self,type='default',user_pre=None,userdict_path=None,stop_words_path=None,words=None,params={}):
        '''
        type 'user':user_pre callable,params
        type 'default':userdict_path,stop_words_path,words
        type 'None':do Nonthing
        '''
        self.dict=userdict_path
        if self.dict!=None:
            jieba.load_userdict(self.dict)
        
        self.stop_words=['',' ','  ','\n','\r','\t']
        if stop_words_path!=None:
            self.stop_words=self.stop_words+[i.strip() for i in open('stop_words_path','r')]
        self.stop_words=set(self.stop_words)
        self.params=params
        if words!=None:
            self.words=set(words)
        else:
            self.words=None
        
        if type=='user':
            self.pre=user_pre
        elif type=='default':
            self.pre=partial(default_preprocess,stop_words=self.stop_words,words=self.words)
        elif type=='None':
            self.pre=lambda x:x.strip()

    def transform(self,X):
        if type(X)==type([1,2]):
            X_new=[self.pre(i) for i in X]
            #TODO: 由于一开始分词肯定是没有vocabulary的，所以不能使用vocabulary。
        elif type(X)==type('xxx'):
            X_new=[self.pre(X)]#ext input must a list
        return X_new

    def fit(self,X,y=None):
        return self

    def get_params(self,deep=True):
        return {}
        
def default_preprocess(x,lang='cn',stop_words=[],words=None):
    '''
    x=re.sub(r'\(\S+?\)','',x)
    x=re.sub(r'（\S+?）','',x)
    x=re.sub(r'\[\S+?\]','',x)
    x=re.sub(r'【\S+?】','',x)
    x=re.sub(r'http:[/\w\.]+','',x)
    '''
    x=re.sub(r' \d+\.?\d* ', ' ', x)
    #就写了几个，期望有人把预处理的正则补齐
    if lang=='cn':
        cut=lambda x:jieba.cut(x)
    elif lang=='en':
        cut=lambda x:x.spilt(' ')
    if words==None:
        con=lambda x:x not in stop_words
    else:
        con=lambda x:(x in words) and (x not in stop_words)
    x=' '.join(filter(con,[w.encode('utf-8') for w in cut(x)]))
    return x

