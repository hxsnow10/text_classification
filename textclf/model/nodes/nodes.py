# -*- coding: utf8
from makenodes import *

class node:
    def __init__(self,ntype,name,obj,nexts):
        self.ntype=ntype
        self.name=name
        self.obj=obj
        self.nexts=nexts

def search(name,input_params):
    try:
        anode=nodes_list[name]#是否一定会有
    except:
        print 'no '+name+' in '+'nodes_list'
        return
    if anode.ntype=='f':
        params={}
        for para in anode.nexts:
            pname=para.split('.')[-1]
            value=search(para,input_params)
            if value!='sys_default':
                    params[pname]=value
        return (anode.obj)(**params)
    elif anode.ntype=='s':
        return search(input_params[name],input_params)
    elif anode.ntype=='na':#ask a str and return str
        if name in input_params:
            return input_params[name]
        else:
            return 'sys_default'
    elif anode.ntype=='nn':#no ask return obj
        return anode.obj
# so when 

#逻辑上，每个节点可以search,search返回一个对象，在一些位置（即需要直接给出选项的地方)需要ask.
#每个节点都可以search;search的过程中需要一些ask.在真叶子，search的直接结果就是返回obj.在loss这样的地方，可以ask。
#loss的地方，肯定要返回loss=obj
#为了简化，不设置真叶子节点，先实现。

#就是说'f'表示函数，'s'表示选择器，'n'表示参数
#比如说一个功能要不要，那么分支为0. select()  1. None
def search_client(name):
    params={}
    anode=nodes_list[name]
    if anode.ntype=='f':
        for para in anode.nexts:
            more=search_client(para)
            if more!=None:
                params=dict(params, **more)
    elif anode.ntype=='s':
        params[anode.name]=ask(anode.name,anode.nexts)
        more=search_client(params[anode.name])
        if more!=None:
            params=dict(params,**more)
    elif anode.ntype=='na':
        params[name]=ask(anode.name)
    elif anode.ntype=='nn':
        pass
    return params

def ask(key,values=[]):
    #这应该是客户实现的部分，即函数的参数是一次性获取的，
    #.search在客户端走一遍，包含ask()，返回一个选择的list（即路径)，然后再在服务器段走一遍，返回一个对象
    #即ask()在服务器与客户端并不相同，前以确定参数为输入，后等待人的即时输入
    
    #需要继续做
    if len(values)==1:
        return values[0]
    for i in values:
        print i,
    return input_params('choose a value')
    '''
    if values==[]:
        fp.write('None'+'\n')
        return None
    else:
        fp.write(values[0]+'\n')
        return values[0]
    '''
