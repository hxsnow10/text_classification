#encoding=utf-8
from textclf.model.packs import *
from textclf.data import *
import numpy as np

def Makedata(X,y,data_split=[('train',1)]):
    '''
    for pylearn2 training
    '''
    left,sum=0,len(y)
    for name,frac in data_split:
        right=frac
        if y!=[]:
            np.save(name+'_y.npy',y[int(left*sum):int(right*sum)])
            print 'saved '+name+'_y.npy'
        np.save(name+'_X.npy',X[int(left*sum):int(right*sum)])
        print 'saved '+name+'_X.npy'
        left=right
