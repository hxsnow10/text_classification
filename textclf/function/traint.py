#encoding=utf-8
import os

from .train_nn import Train_nn
from .train import Train
from .test_nn import Test_nn
from .test import Test

def TrainT(data_path=None,report_path=None,raw_params={'type':'label'},pre_params={'type':'default'},tmodel=None,model_params={},pfrac=0.1,only_test=0, debug_params={"samples":-1},check=1,nn=0):
    '''
    Train and Predict to data.
    
    parameters
    ----------
    Refer Train and Test.

    pfrac:float.(1-pfrac)*data as train_data for Train, pfrac*data as test_data for Test.
    
    only_test:default 0.0:train and test.1:only test pfrac*data.
    
    debug_params:{"samples":n} n is the number of error test to debug.

    check:default 1.check before pre and train.

    
    return
    ----------
    retun None

    genrated report directory:
    report_path:
        -test_data
        -train:
            -
            ...
        -test:
            -
            ...
    '''
    if nn==1:
        train_=Train_nn
        test_=Test_nn
    else:
        train_=Train
        test_=Test
    
    if only_test==1:
        Test(test_data=report_path+'/test_data',report_path=report_path+'/test',raw_params=raw_params,model_path=report_path+'/train/model',debug_params=debug_params)
        return
    
    try:
        os.makedirs(report_path)
    except:
        print "原本的报告被覆盖了"
    fp=open(data_path,'r')
    lines=list(fp.readlines())
    n=len(lines)
    train_lines,test_lines=lines[0:int((1-pfrac)*n)],lines[int((1-pfrac)*n):-1]
    fp.close()
     
    train_data=open(report_path+'/train_data','w')
    for i in train_lines:
        train_data.write(i)
    train_data.close()
    train_(data_path=report_path+'/train_data',report_path=report_path+'/train',raw_params=raw_params,pre_params=pre_params,tmodel=tmodel,model_params=model_params,check=check)
   #TODO: rm train_data 
    
    test_data=open(report_path+'/test_data','w')
    for i in test_lines:
        test_data.write(i)
    test_data.close()
    test_(test_data=report_path+'/test_data',report_path=report_path+'/test',raw_params=raw_params,model_path=report_path+'/train/model',debug_params=debug_params,check=check)
    
