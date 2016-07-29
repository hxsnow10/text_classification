#encoding=utf-8
from textclf.data import *
from textclf.model.packs import *
from textclf.vocab.words import Vocabulary

vocab=Vocabulary(input_dir='all_weibo.vocab')
word_sent=vocab.attr['sentiment']
#filter_words=[w for w in vocab.words if word_sent[w]=='-1' or word_sent[w]=='1']
filter_words=vocab.words
print len(filter_words)
X,y,_=raw().transform('all_label')
X=Preprocess(words=filter_words).transform(X)
X,y=IndexSequenceTransformer(sen_len=50,words=vocab.words).transform(X,y)#允许词典中有非极性词，在分词的时候把非极性词过滤

Makedata(X,y,data_split=[('train',0.9),('valid',0.99),('test',1)])
