#encoding=utf-8
import numpy as np
import os
from jieba import posseg
from collections import OrderedDict
from gensim.models import word2vec
'''
may Bug:
update_word_attr('vector',attr_dict)之后，word_vecotr写的映射出错了，？？

'''

def _load_word_vector(file):
    fp=open(file,'r')
    word_vector=OrderedDict()
    for line in fp:
        try:
            seg = line.strip().split(' ')
            assert len(seg)>10
            word,vector=seg[0],[float(i) for i in seg[1:]]
            word_vector[word]=vector
        except:
            print line
    return word_vector

def Load_vocabulary_from_vectors(vectors_file,output_dir,name=''):
    word_vector=_load_word_vector(vectors_file)
    words=[word for word in word_vector]
    v=Vocabulary(output_dir=output_dir, words=words , word_vector=word_vector, vec_len=200, name=name)
    return v

class Vocabulary():
    '''
    词典。在常见的机器学习过程中，用词典对语料词进行约束。

    Params
    ----------
    vocabulary: OrderDict/Dict. 如果没有词向量，这就是核心的词典 str(word):int(index)。
    word_vec: OrderedDict  str(word):float_list(vector).
    vectors:a numpy matrix.
    vec_len: len of vector.

    word_vec 可以生成vectors与vocabulary
    vectos与vocabulary也能生成word_vec
    row: bool. 
    '''

    def __init__(self,name='', words=None, input_dir=None, output_dir=None, word_flag={}, word_vector={}, word_sentiment={}, vec_len=200, w2v=False):
        if input_dir!=None:
            self.vec_len=vec_len
            self.load(input_dir,w2v)
            self.output_dir=input_dir
            return
        
        self.name=name
        self.output_dir=output_dir
        self.words=words
        
        #index
        _word_index={w:i for i,w in enumerate(words)}
        
        #flag
        _word_flag=OrderedDict()
        for w in words:
            if w in word_flag:
                _word_flag[w]=word_flag[w]
            else:
                _word_flag[w]=self.get_flag(w)

        #vector
        _word_vector=OrderedDict()
        for w in words:
            if w in word_vector:
                _word_vector[w]=word_vector[w]
            else:
                _word_vector[w]=np.zeros((vec_len))
        
        #sentiment
        _word_sentiment=OrderedDict()
        for w in words:
            if w in word_sentiment:
                _word_sentiment[w]=word_sentiment[w]
            else:
                _word_sentiment[w]='u'
        
        self.attr={'index':_word_index, 'flag':_word_flag, 'vector':_word_vector, 'sentiment':_word_sentiment}
        self.vec_len=vec_len
        self.vectors=self._vectors(_word_vector)
        
        if output_dir!=None:
            self.save()
        
    def update_words(self, words={},mode='pluse'):
        '''
        mode='pluse','replace'
        '''
        old_words=self.words
        if mode=='replace':
            self.added_words=added_words=set(words)-set(old_words)
            self.deleted_words=deleted_words=set(old_words)-set(words)
            self.words=words
        elif mode=='pluse':
            self.added_words=added_words=set(words)-set(old_words)
            self.deleted_words=deleted_words=set([])
            self.words=self.words+list(added_words)
        
        for w in added_words:
            self.attr['flag'][w]=self.get_flag(w)
            self.attr['vector'][w]=np.zeros((self.vec_len))
            self.attr['sentiment'][w]='u'
            
        for w in deleted_words:
            del self.attr['flag'][w]
            del self.attr['vector'][w]
            del self.attr['sentiment'][w]
            
        for i,w in enumerate(self.words):
            self.attr['index'][w]=i
            
        self.vectors=self._vectors(self.attr['vector'])
    
    def update_word_attr(self, attr_name, attr_dict, mode='pluse'):
        words=attr_dict.keys()
        self.update_words(words, mode=mode)
        print self.words[0],self.words[1]
        for w in attr_dict:
            self.attr[attr_name][w]=attr_dict[w]
        print self.words[0],self.words[1]
    
    def _vectors(self,word_vector):
        if word_vector==None:
            return None
        vectors=[word_vector[w] for w in word_vector]
        #'''debug
        for i in word_vector:
            if len(word_vector[i])!=self.vec_len:
                print i,word_vector[i],len(word_vector[i])
        #'''
        vectors=np.asarray(vectors,dtype=np.float32)
        return vectors
    
    def _vectors_back(vectors,words):
        '''
        generate word:vec Dict from word_vec_npy and word:index vocabulary
        '''
        word_vector=OrderedDict()
        for index,word in enumerate(words):
            word_vec[word]=word_vector[index]
        return word_vector

    def get_flag(self, word):
        return list(posseg.cut(word))[0].flag
    
    def save(self, output_dir=None):
        if output_dir==None:
            output_dir=self.output_dir
        output_dir+='/'
        if not os.path.exists(output_dir):
            os.system('mkdir '+output_dir)
        
        self._save_words(output_dir+'words.txt')
        self._save_word_attr(output_dir+'word_flag.txt',self.attr['flag'],split='\t')
        self._save_word_attr(output_dir+'word_vector.txt',self.attr['vector'],attr_name='vector', split=' ')
        self._save_word_attr(output_dir+'word_sentiment.txt',self.attr['sentiment'],split='\t')
        np.save(output_dir+'vectors.npy',self.vectors)
    
    def load(self, output_dir, w2v):
        if output_dir==None:
            output_dir=self.output_dir
        output_dir+='/'
        if not os.path.exists(output_dir):
            #raise Error()
            print 'xxxxxxxxxxx'
            return
        self.attr={} 
        self.words=self._load_words(output_dir+'words.txt')
        self.attr['index']={w:i for i,w in enumerate(self.words)}
        self.attr['flag']=self._load_word_attr(output_dir+'word_flag.txt',split='\t')
        self.attr['vector']=self._load_word_attr(output_dir+'word_vector.txt',attr_name='vector', split=' ')
        self.attr['sentiment']=self._load_word_attr(output_dir+'word_sentiment.txt',split='\t')
        self.vectors=np.load(output_dir+'vectors.npy')
        if w2v:
            self.w2v_model=word2vec.Word2Vec.load_word2vec_format(output_dir+'word_vector.txt',binary=False)
    
    def _load_words(self, file):
        fp=open(file,'r')
        num=int(fp.readline().strip())
        words=[]
        for line in fp:
            word=line.strip()
            words.append(word)
        assert num==len(words)
        return words
    
    def _save_words(self, file):
        fp=open(file,'w')
        fp.write(str(len(self.words))+'\n')
        for w in self.words:
            fp.write(w+'\n')
        fp.close()
    
    def _load_word_attr(self, file, attr_name='', split='\t'):
        fp=open(file,'r')
        if attr_name=='vector':
            fp.readline()
        attr_dict=OrderedDict()
        for line in fp:
            a=line.strip().split(split)
            word=a[0]
            if attr_name=='vector':
                value=[float(i) for i in a[1:]]
            else:
                value=a[1]
            attr_dict[word]=value
        return attr_dict
    
    def _save_word_attr(self, file, attr_dict, attr_name='', split='\t'):
        fp=open(file,'w')
        if attr_name=='vector':
            fp.write(str(len(self.words))+' '+str(self.vec_len)+'\n')
        for w in attr_dict:
            if attr_name=='vector':
                value=' '.join([str(i) for i in attr_dict[w]])
            else:
                value=attr_dict[w]
            fp.write(w+split+value+'\n')
        fp.close()
