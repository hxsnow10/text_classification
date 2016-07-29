# -*- coding: utf8
#这个文件依赖node.py生成所需要的nodes_list,与主程序的关系仅仅通过nodes_list.
#我们需要让它生出正确的nodes_list树，nodes_list本质上描述了一个可组织的可输入的逻辑对象
from ..packs import *

class node:
    def __init__(self,ntype,name,obj,nexts):
        self.ntype=ntype
        self.name=name
        self.obj=obj
        self.nexts=nexts

def update(name,ntype,obj=None,nexts=None):
    if ntype=='f':
        if (name!='Pipeline.steps'):
            params=instance[name].get_params(False)
            for i in params:
                iname=name+'.'+i
                if iname not in nodes_list:
                    update(iname,'na')
                else:
                    print iname+' has corred'
            '''
            if iname in bad:
                bad[iname].append(name)
            else:
                bad[iname]=[name]
            '''
        
        if nexts==None:
            nexts=list(name+'.'+i for i in params.keys())
    nodes_list[name]=node(ntype,name,obj,nexts)
    
instance={
    'GridSearchCV':GridSearchCV(LogisticRegression(),{}),
    'Pipeline':Pipeline([('clf',LogisticRegression())]),
    
    'CountVectorizer':CountVectorizer(),'HashingVectorizer':HashingVectorizer(),'TfidfVectorizer':TfidfVectorizer(),
    'SelectKBest':SelectKBest(), 
    'GenericUnivariateSelect':GenericUnivariateSelect(),
    'RFE':RFE(LogisticRegression()),
    'RFECV':RFECV(LogisticRegression()),
    'VarianceThreshold':VarianceThreshold(),
    
    'LogisticRegression':LogisticRegression(),'SGDClassifier':SGDClassifier(),
    'SVC':SVC(),'NuSVC':NuSVC(),'LinearSVC':LinearSVC(),
    'DecisionTreeClassifier':DecisionTreeClassifier(),
    'BaggingClassifier':BaggingClassifier(),'AdaBoostClassifier':AdaBoostClassifier(),'RandomForestClassifier':RandomForestClassifier(),#,'GradientBoostingClassifier':GradientBoostingClassifier(),
    'MultinomialNB':MultinomialNB(),
    'KNeighborsClassifier':KNeighborsClassifier()
    }
    

#functions  F
functions=[
    GridSearchCV,
    Pipeline,
    CountVectorizer,HashingVectorizer,TfidfVectorizer,
    GenericUnivariateSelect,RFE,RFECV,VarianceThreshold,SelectKBest,
    LogisticRegression,SGDClassifier,
    SVC,NuSVC,LinearSVC,
    DecisionTreeClassifier,
    BaggingClassifier,AdaBoostClassifier,RandomForestClassifier,#GradientBoostingClassifier,
    MultinomialNB,
    KNeighborsClassifier
    
    ]

#make selector nodes   S
selectors={
    'GridSearchCV.estimator':['Pipeline'],
    'steps.ext':['CountVectorizer','HashingVectorizer','TfidfVectorizer'],#to add 
    'steps.sel':['GenericUnivariateSelect','RFE','RFECV','VarianceThreshold','SelectKBest'],
    'steps.clf':['LogisticRegression','SGDClassifier',
            'SVC','NuSVC','LinearSVC',
            'DecisionTreeClassifier',
            'BaggingClassifier','AdaBoostClassifier','RandomForestClassifier',#'GradientBoostingClassifier',
            'MultinomialNB',
            'KNeighborsClassifier']
}

NNs={
    'SelectKBest.score_func':chi2
    }

#------------------------------------------------------
#make nodes_list
def yyyy(ext=None,sel=None,clf=None):
    return[('ext',ext),('sel',sel),('clf',clf)]

nodes_list={}
#make function nodes
#by the way, make na nodes
for i in functions:
    update(i.__name__,'f',obj=i) 
update('Pipeline.steps','f',obj=yyyy,nexts=['steps.ext','steps.sel','steps.clf'])

#make selector nodes
for i in selectors:
    update(i,'s',nexts=selectors[i])

#make nn nodes
for i in NNs:
    update(i,'nn',NNs[i],[])

'''
fp=open('.main_keys_values','w')
fp.write('MAIN_KEYS_VALUES\n'+'-'*20+'\n')
fp.write('Here show keys and values for model_params\n')
fp.write('\t1. Keys include following s(selector)(must provided) and \n\tall function leave params(not show following, refer to sklearn\n')
fp.write('\t2. selector key related values is the indent string;leave params ralated values refer to sklearn\n\n')
def print_tree(name,n):
    anode=nodes_list[name]
    if anode.ntype!='na':
        fp.write(n*'\t'+name+'\t'+str(anode.ntype)+'\n')
    if anode.nexts!=None:
        for i in anode.nexts:
            print_tree(i,n+1)
    #print nodes_tree
print_tree('GridSearchCV',0)
fp.close() 
'''

#pdump('nodes_list_s',nodes_list)
