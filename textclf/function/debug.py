#encoding=utf-8
from .predict import *


import collections
import json

def Debug(data,report_path,model_path,dtype='path',raw_params={'type':'label'},index_list=None,index_path=None):
    '''
    output data stream for defined data and process.

    parameters
    ------------------
    其他都一样啊...
    index_lis,index_path定义了2种指派index的方式。

    '''
    if index_list!=None:
        index=index_list
    if index_path!=None:
        fp=open('index_path','r')
        lines=fp.readlines()
        index=list(int(i) for i in lines)
        fp.close()

    model=pload(model_path)
    ext=model.get_params()['ext']
    
    if dtype=='path':
        X,y,_=get_raw(data,dtype,raw_params)
        debug_X=list(X[i] for i in index)
    else:
        debug_X=[data] 
    fp=open(report_path,'w')
    for i in debug_X:
        ans=Predict(model,i,debug=1)
        fp.write('-'*30+'\ndata_flow\n')
        for step in ans:
            fp.write('\n')
            fp.write(step+':\n')
            if step in ['raw','pre']:
                fp.write(ans[step]+'\n')
            if step in ['feature extraction','feature selection']:
                for word in ans[step]:
                    fp.write(word+str(ans[step][word])+'\n')
            if step in ['clf']:
                for k in ans[step]:
                    if k!='feature_importance':
                        fp.write(k+str(ans[step][k])+'\n')
                    else:
                        fp.write(k)
                        for word in ans[step][k]:
                            fp.write(word+str(ans[step][k][word])+'\n') 
        fp.write('\n') 
    fp.close()

    return None

