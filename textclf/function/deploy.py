#encoding=utf-8
import subprocess
import os

from ..util.pick import *

def Deploy(model_path,model_name):
    '''
    
    '''
    models_dir='/root/xia.hong/text_platform_service/server/plugins/classifer/'
    new_model_dir=model_dir+model_name
    os.makedirs(new_model_dir)
    
    model=pload(model_path)
    
    old_dict_path=model.get_params()['pre'].dict
    if old_dict_path!=None:
        new_dict_path=new_model_dir+'user.dict'
        model.get_params()['pre'].dict=new_dict_path 
        cmd='cp '+old_dict_path+' '+new_dict_path+'/user.dict'
        subprocess.call(cmd)
 
    pdump(new_model_dir+'/model',model)
