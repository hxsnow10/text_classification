#encoding=utf-8
import numpy as np
from textclf.vocab.words import Vocabulary
import cPickle as pickle

model=pickle.load(open('best_model.pkl','r'))
vec=model.get_param_values()[0]
old_vec=open('jd_weibo_sent/word_vector.txt','r')
new_vec=open('new_vector.txt','w')
old_vec.readline()
for i in range(len(vec)):
    line=old_vec.readline()
    word=line.split(' ')[0]
    s=' '.join([word]+[str(e) for e in vec[i].tolist()])
    new_vec.write(s+'\n')
