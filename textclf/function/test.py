#encoding=utf-8
import os

from sklearn.metrics import classification_report
from ..util.pick import *
from ..model import *
from ..data import *
from getmethod import *
from debug import Debug
from .predict import Predict
import dill
import readline

def Test(test_data,report_path,raw_params={'type':'label'},model_path=None,dtype='path',debug_params={},check=1):
    '''
    Parameters
    -----------
    test_data:str
    represents data_path(dtype='path') or data str(dtype='line')
    
    report_path:str
    path of report directory

    model_path:str
    path of the model object to pickle.load.

    debug_params:a dict
        'samples':n,-1.the number of error of debug.
        'debug_nodes':list.could be 'pre','ext','sel','clf' TODO 
    
    check:0/1.
    when check=0, no GO y/n will asked.
    
    Return
    -----------
    function return 
        dict{
            #init
            'test_data':
            'dtype':
            'report_path':
            'model_path':
            #result
            'y':
            'pre_y':
            'metrics':
        }
   some files will saved to report_path
    Report_path
        -report:    readable report
        -ans:       reable ANS
        -stream     debug output
        -index_of_errory    index of error_y
    '''
    print '\nTEST\n'+'-'*40
    print '0. load model'
    model=pload(model_path)
    print '\n1. get_raw of data'
    raw_X,raw_y,illegal_index=get_raw(test_data,dtype,raw_params=raw_params)
    print 'lne X=',len(raw_X)
    print 'len y=',len(raw_y)
    if checkouty(raw_y,check)=='n':
        return None
    X,y=raw_X,raw_y
    print '\n2. test'
    pre_y=model.predict(raw_X)
    print '\n3. save result'
    result={
        #init
        'test_data':test_data,
        'dtype':dtype,
        'report_path':report_path,
        'model_path':model_path,
        #result
        'pre_y':pre_y,
        'y':y,
        'illegal_index':illegal_index
        }
    if y!=[]:
        result['metrics']=classification_report(y,pre_y)
        result['index_of_errory']=list(i for i in range(len(X)) if y[i]!=pre_y[i])
        print 'num of errory',len(result['index_of_errory'])
    if test_save_local_result(result)==None:
        return None
    if debug_params!={}:
        n=debug_params['samples']
        if n==-1:
            n=10000000
        debug_indexs=list(i for i in range(len(X)) if y[i]!=pre_y[i])
        debug_index=debug_indexs[0:min(n,len(debug_indexs))]
        Debug(test_data,report_path+'/stream',model_path,dtype=dtype,raw_params=raw_params,index_list=debug_index)
    return result

def test_save_local_result(result):
    try:
        os.makedirs(result['report_path'])
        print 'preport' 
    except OSError, why :
        print 'report directory will cover original'
        '''
        s=raw_input('Cover? y/n')
        if s=='n':
            return None
        '''
    model=pload(result['model_path'])
    pdump(result['report_path']+'/result',result)
    
    fp=open(result['report_path']+'/report','w')
    fp.writelines((i+'\n' for i in[
        'Predict Report',
        '-'*20,
        '[init]'
        'test_data'+' = '+str(result['test_data']),
        'model_path'+' = '+result['model_path'],
        '[result]'
        'test_ans_path'+' = :./ans',
        'result_path'+'=./result' 
        ]))
    if 'metrics' in result:    
		fp.write('metrics'+' =\n'+str(result['metrics'])+'\n')
    fp.close()
    
    pre_y=result['pre_y'].tolist()
    for i in result['illegal_index']:
        pre_y.insert(i,'illegal')

    fp=open(result['report_path']+'/pre_y','w')
    fp.write('len='+str(len(pre_y))+'\n')
    for i in range(len(pre_y)):
        fp.writelines(str(pre_y[i])+'\n')
    fp.close()
    
    if 'metrics' in result:    
        error_y=result['index_of_errory']
        fp=open(result['report_path']+'/index_of_errory','w')
        for i in error_y:
            fp.write(str(i)+'\n')
        fp.close()

    return True

