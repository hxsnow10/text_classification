#encoding=utf-8
from getmethod import *
from ..model import *
from ..data import *
from ..util import *
import collections
import json

def Predict(model,X,proba=0,debug=0):
    '''
    意思自明。
    model 是模型对象。
    X可以为List或者一个content。
    proba表示是否输出proba结果。
    debug表示是否输出debug结果,若debug=1,无视proba
    '''
    if proba==0 and debug==0:
        if type(X)==type('www'):
            return model.predict([X])[0]
        else:
            return model.predict(X)
    if proba==1 and debug==0:
        if type(X)==type('www'):
            return model.predict_proba([X])[0]
        else:
            return model.predict_proba(X)    
    else:
        if type(X)==type('www'):
            return data_flow(X,model)
        else:
            return list(data_flow(x,model) for x in X)


def data_flow(x,model,simple=0):
    '''
    x is the preprocess str
    这里没有提供x是list的接口，可能是因为处理[list]时会多一些复杂度。
    如果想要list的，可以在外面套个接口list(data_flow(x,model) for x in X)
    
    '''
    if simple==1:
        result={}
        try:
            print x
            result['proba_y']=model.predict_proba([x])[0].tolist()
            print result['proba_y']
        except:
            pass
        result['y']=model.predict([x])[0]
        return result

    steps=[
        ('pre',model.get_params()['pre'].transform),
        ('feature extraction',model.get_params()['ext'].transform),
        ('feature selection',model.get_params()['sel'].transform),
        ('clf',#[model.get_params()['clf'].predict_proda,
                model.get_params()['clf'].predict)
        ]
    data=x#[x]会报错
    debug_stream=collections.OrderedDict()
    debug_stream['raw']=data
    invoc=[]
    col=[]
    for f in steps:
        data=f[1](data)
        readable=collections.OrderedDict()
        if f[0]=='pre':
            readable=data[0] 
        if f[0]=='feature extraction':
            ext=model.get_params()['ext']
            voc=ext.vocabulary_
            invoc={v:k for k,v in voc.items()}
            obj2=data.asformat('coo')
            col=obj2.col
            data2=obj2.data
            for j in range(len(col)):
                readable[invoc[col[j]]]=data2[j]
        if f[0]=='feature selection':
            sel=model.get_params()['sel']
            voc=sel.get_support(True)
            obj2=data.asformat('coo') 
            col=obj2.col
            data2=obj2.data
            for j in range(len(col)):
                readable[invoc[voc[col[j]]]]=data2[j]
        if f[0]=='clf':
            featurei=[]
            feature=getfeature(model)
            importance=getimportance(model)
            clf=model.get_params()['clf']
            if clf.__class__.__name__ in ['DecisionTreeClassifier','RandomForestClassifier']:
                for i in col:
                    featurei.append((feature[i],importance[i]))
                featurei=sorted(featurei,key=(lambda x : x[1]),reverse=True)

                
            elif clf.__class__.__name__ in ['LogisticRegression','SGDClassifier','LinearSVC','MultinomialNB']:
                n=len(importance)
                for i in col:
                    ss=[]
                    for j in range(n):
                        ss.append(importance[j][i])
                    featurei.append((feature[i],ss))
                featurei=sorted(featurei,key=(lambda x : x[1][0]),reverse=True)
            readable['feature_importance']=collections.OrderedDict()
            for i in featurei:
                readable['feature_importance'][i[0]]=i[1]
            try:
                readable['proba_y']=model.predict_proba(x)[0].tolist()
            except Exception as e:
                print 'error=', e
            
            readable['y']=data[0]
        debug_stream[f[0]]=readable
    #print str(debug_stream)
    return debug_stream
