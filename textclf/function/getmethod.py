#encoding=utf-8
from ..model.packs import * 

def getfeature(model,name=None):
    tmpdict=dict([(v,k) for (k,v) in model.get_params()["ext"].vocabulary_.iteritems()])
    clf=model.get_params()["clf"]
    tmpindex=model.get_params()['sel'].get_support(True)
    features=[]
    for i in tmpindex:
        features.append(tmpdict[i])
    return features

def name(model):
    return str(type(d)).split('.')[-1]

def getimportance(model,name=None):#TODO 注意输出的shape！
    coef_name=['LogisticRegression','SGDClassifier','LinearSVC','MultinomialNB']#Multino..  直接的是使用feature_log_prob_
    feature_importance_name=['AdaBoostClassifier','GradientBoostingClassifier','RandomForestClassifier','DecisionTreeClassifier']
    dual_name=['SVC','NuSVC']
#BaggingClassifier 没有feature_importance属性因为他基础分类器是黑箱子，需要自己去定义
    clf=model.get_params()['clf']
    if clf.__class__.__name__ in coef_name:
        return clf.coef_
    elif clf.__class__.__name__ in feature_importance_name:
        return clf.feature_importances_
    elif clf.__class__.__name__=='GaussianNB':
        return list((clf.theta[i][j],clf.sigma[i][j]) for i in range(len(clf.theta_)) for j in range(len(clf.theta[0])))

    #elif name(model) in dual_name:
    #    return trans(model.dual_coef_)#TODO

def getgeneralattr(model,name=None):
    return getattr(model,name+'_')

def getmethod(name):    
    if name=='feature':return getfeature
    elif name=='importance':return getimportance
    else:return getgeneralattr


