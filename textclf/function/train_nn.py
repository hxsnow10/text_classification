#encoding=utf-8
'''
API for text_classfication
'''
import os
import copy
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
sys.setrecursionlimit(10000)
from sklearn.metrics import classification_report
from ..data import *
from ..model import *
from ..util import *
from getmethod import *

def Train_nn(data_path=None,report_path=None,raw_params={'type':'label'},pre_params={'type':'default'},tmodel=None,model_params={},check=1):
    print data_path
    try:
        os.makedirs(report_path)
    except:
        print 'report directory will cover original'
    print '\nTRAIN\n'+'-'*40
    
    print '0. build tmodel=pipeline(ext,sel,clf)'
    if tmodel==None:
        tmodel=search('GridSearchCV',model_params)
    clf=tmodel.get_params()['clf']
    clf.outputmodel=report_path+'/model'
    print '\n1. get_raw of data'
    raw_X,raw_y,illegal_index=get_raw(data_path,dtype='path',raw_params=raw_params)
    print 'len X,y='+str(len(raw_X))
    if checkouty(raw_y,check)=='n':
        return None 
    print '\n2. preprocess'
    #将pre从pipeline中分离出来是考虑到pre耗时很大，在pipeline中也许没有优化的措施
    pre=Preprocess(**pre_params)
    X,y=pre.transform(raw_X),list(int(yy) for yy in raw_y)
    print len(X),len(y)
    print '\n3. train'
    tmodel.fit(X,y)
    model=tmodel    
    pre_y=model.predict(X)
    if y!=[]:
        fp=open(report_path+'/report','w')
        fp.write('metrics=\n'+classification_report(y,pre_y)+'\n')
        fp.close()
    return {}
