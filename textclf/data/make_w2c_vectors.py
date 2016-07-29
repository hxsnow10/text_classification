#encoding=utf-8
from textclf.model.packs import *
from textclf.data import *
import gensim,logging

def make_w2c_vectors(data_path,save_name,raw_params={'type':'label'},pre_params={},size=200,window=5,min_count=5,iter=2,other_params={}):
    '''
    use gensim.models.Word2Vec to train word embeddings
    '''
    
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    print '\n1. get_raw'
    rawer=raw(**raw_params)
    X,y,_=rawer.transform('data')

    print '\n2. preprocess'
    pre=Preprocess(**pre_params)
    X=pre.transform(X)
    sentences=list(sent.split(' ') for sent in X)

    print '\n3.make w2c vectors'
    model = gensim.models.Word2Vec(sentences, size=200,window=5, min_count=10, iter=2 )
    model.save(save_name+'.model')
    model.save_word2vec_format(save_name+'.txt')

