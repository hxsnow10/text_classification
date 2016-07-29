from textclf.data import *
from textclf.model.packs import *
from textclf.vocab.words import Vocabulary
import readline
import time
import sys

#argv[1] vocab
#argv[2] model
#argv[3] count

vocab=Vocabulary(input_dir='all_weibo.vocab',vec_len=200)
#filter_words=[i for i in vocab.words if vocab.attr['flag'][i]!=0]
pre=Preprocess()
ext=IndexSequenceTransformer(sen_len=50,words=vocab.words)
clf=Pylearn2_model('best_model.pkl')
while True:
    inputs=[raw_input('Enter Contents:')]
    X=pre.transform(inputs)
    X,_=ext.transform(X)
    y=clf.transform(X,proba=True)
    print y[0]
    
