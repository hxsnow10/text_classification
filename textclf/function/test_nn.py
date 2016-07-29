#encoding=utf-8
import os

from sklearn.metrics import classification_report
from ..util.pick import *
from ..model import *
from ..data import *
from getmethod import *
from debug import Debug
from .predict import Predict

def Test_nn(test_data,report_path,model_path,raw_params={'type':'label'},dtype='path',debug_params=None,check=1):
    print '\nTEST\n'+'-'*40
    print '0. load model'
    ext=W2cTensor()
    sel=EqualSelect()
    clf=Cnn1(model_path=model_path)
    model=Pipeline([
        ('ext',ext),
        ('sel',sel),
        ('clf',clf)
        ])
    print '\n1. get_raw of data'
    raw_X,raw_y,illegal_index=get_raw(test_data,dtype,raw_params=raw_params)
    print 'lne X=',len(raw_X)
    print 'len y=',len(raw_y)
    if checkouty(raw_y,check)=='n':
        return None
    X,y=raw_X,list(int(yy) for yy in raw_y)
    print '\n2. test'
    pre_y=model.predict(raw_X)
    print '\n3. save result'
    
    try:
        os.makedirs(report_path)
    except OSError, why :
        print 'report directory will cover original'
    
    fp=open(report_path+'/pre_y','w')
    fp.write('len='+str(len(pre_y))+'\n')
    for i in range(len(pre_y)):
        fp.writelines(str(pre_y[i])+'\n')
    fp.close()


    if y!=[]:
        fp=open(report_path+'/report','w')
        fp.write('metrics=\n'+classification_report(y,pre_y)+'\n')
        fp.close()
