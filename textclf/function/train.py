#encoding=utf-8
'''
API for text_classfication
'''
import os
import copy
import sys
import dill
import readline
reload(sys)
sys.setdefaultencoding( "utf-8" )
sys.setrecursionlimit(10000)

from sklearn.metrics import classification_report
from ..data import *
from ..model import *
from ..util import *
from getmethod import *
coefs_list={
'all':['feature','importance']
}

def Train(data_path=None,report_path=None,raw_params={'type':'label'},pre_params={'type':'default'},tmodel=None,model_params={},check=1):
    '''    
    Pramaters
    ------------- 
    data_path:str.
    path of train data file.
    
    report_path:str.
    path of report directory.
    
    raw_params:dict.
    way to get_raw.
    keys:
        'type':str.'label' or 'unlabel' or 'user' . seem 'user' is unused.
        'raw':str.user_defined raw object.
    
    pre_params:dict. 
    a dict to build preprocessor.Preprocessor take documentation vector as input and (X,y) as output.
    dict keys may include keys:type,pre_path,params,userdict_path.
        'type':str.'default','user'.'default' generate a build_in precossor, with params includes 'lang'.'user' pickle.loads 'path' relative model.all load pre model should work like this: pre(line,**params)
        'path':str.when type=='user', defiened pre model path.
        'userdict_path':str.path for Both type of preprocess.
        'stop_words_path':str.#not supported now.
        'params':dict.param dict for specifilly generated pre.
            build_in pre support 'lang'='en' or 'cn'.default 'cn'.
            
    
    tmodel:tmodel object.one of thr init method for tmodel(the model used to fit(X,y)).
    
    model_params:dict.includes params for build GridSearchCV().Refer to main_kays_values.two types of keys is supported.
    
    Return
    ----------
    a dict includes various information.    
        dict{
        #init
        'data_path':,
        'report_path':,
        'tmodel':,
        'model_params':,
        #result
        'model':,
        'nopre_model':,
        'small_model':,
        'small_nopre_model':,
        'score':,
        'super_params':,
        'classes':,
        'coef':
        }
    
    As the sametime some files will saved to report_path.
    report_path
        -report:                Readable report
        -model                  model object, when feature extraction is natural, includes pre.
        -nopre_model:           no-pre, natural ext(feature extraction).
        -small_model:           feature extraction is limited to selected features.(refited).which make model is smaller.
        -small_nopre_model:     no-pre and refited ext.
        -coef:                  feature-importance
    '''
    print '\nTRAIN\n'+'-'*40
    print '0. build tmodel=pipeline(ext,sel,clf)'
    if tmodel==None:
        tmodel=search('GridSearchCV',model_params)
    print '\n1. get_raw of data'
    raw_X,raw_y,illegal_index=get_raw(data_path,dtype='path',raw_params=raw_params)
    print 'len X,y='+str(len(raw_X))
    if checkouty(raw_y,check)=='n':
        return None 
    print '\n2. preprocess'
    #将pre从pipeline中分离出来是考虑到pre耗时很大，在pipeline中也许没有优化的措施
    pre=Preprocess(**pre_params)
    X,y=pre.transform(raw_X),raw_y
    print '\n3. train'
    tmodel.fit(X,y)
    try:
        model=tmodel.best_estimator_
    except:
        model=tmodel
    pre_y=model.predict(X)

    #make model
    model=Pipeline([
        ('pre',pre),
        ('ext',model.get_params()['ext']),
        ('sel',model.get_params()['sel']),
        ('clf',model.get_params()['clf'])
        ])

    #nopre_model
    nopre_model=Pipeline([
        ('ext',model.get_params()['ext']),
        ('sel',model.get_params()['sel']),
        ('clf',model.get_params()['clf'])
        ])
        

    #make small_model
    predict_model=copy.deepcopy(model)
    ext=predict_model.get_params()['ext']
    sel=predict_model.get_params()['sel']
    clf=predict_model.get_params()['clf']
    voc=ext.vocabulary_
    invoc={v:k for k,v in voc.items()}
    k,new_voc=0,{}
    for i in sel.get_support(True):
        new_voc[invoc[i]]=k
        k=k+1
    ext.vocabulary=new_voc
    sel.fit(ext.fit_transform(X,y),y)
    small_model=Pipeline([
            ('pre',pre),
            ('ext',ext),
            ('sel',sel),
            ('clf',clf)
        ])
   
    #small_nopre_model pre
    small_nopre_model=Pipeline([
            ('ext',ext),
            ('sel',sel),
            ('clf',clf)
            ])
    
    print '\n4. save result'
    result={
        #init
        'data_path':data_path,
        'report_path':report_path,
        'tmodel':tmodel,
        'model_params':model_params,
        #result
        'model':model,
        'nopre_model':nopre_model,
        'small_model':small_model,
        'small_nopre_model':small_nopre_model,
        'score':tmodel.best_score_,
        'super_params':_get_params(model,tmodel.param_grid),
        'coef':_get_coefs(model),
    }
        #TODO:other statics

    result['metrics']=classification_report(y,pre_y)
    try:
        result['classes']=model.classes_
    except:
        pass
    train_save_local_result(result)

    print 'successfully Train!\n'
    return result

def _get_params(model,param_grid):
    super_params={}
    s=model.get_params()
    for key in param_grid:
        super_params[key]=s[key]
    return super_params

def _get_coefs(model):
    coefs={}
    for i in coefs_list['all']:
        coefs[i]=getmethod(i)(model,name=i)
    clf=model.get_params()['clf']
    if clf.__class__.__name__ in coefs_list:
        for i in coefs_list[clf.__class__.__name__]:
            coefs[i]=getmothod(i)(model,name=i)
    return coefs

def train_save_local_result(result):
 
    try:
        os.makedirs(result['report_path'])
    except:
        print 'report directory will cover original'
        '''
        s=raw_input('Cover? y/n')
        if s=='n':
            return None
        '''
    pdump(result['report_path']+'/model',result['model'])
    pdump(result['report_path']+'/nopre_model',result['nopre_model'])
    pdump(result['report_path']+'/small_model',result['small_model'])
    pdump(result['report_path']+'/small_nopre_model',result['small_nopre_model'])

    #write report file
    fp=open(result['report_path']+'/report','w')
    fp.write('Train Report\n')
    fp.write('-----------------------------------------------\n')
    try:
        fp.writelines((i+'\n' for i in [
                    '[Train Params]',
                    'data_path='+result['data_path'],
                    'model_params='+str(result['model_params']),
                    '[Train Result]',
                    'model=./model',
                    'score='+str(result['score']),
                    'superParams='+str(result['super_params']),
                    'coefs=./coefs',
                    'metrics=\n'+str(result['metrics'])
                    ]))
    except:
        pass
    fp.close()

    #write coef file
    model=result['model']
    clf=model.get_params()['clf']
    coef=result['coef']
    fp=open(result['report_path']+'/coef',"w")
    clftype=clf.__class__.__name__
    a=coef['feature']
    b=coef['importance']
    fp.write('COEF REPORT\n')
    fp.write('-'*25+'\n')
    fp.writelines(i+'\n' for i in [
        'This is Model:',
        str(clf),
        'Number Of Features Is '+str(len(a))+'\n',
        'All fetures with coefs',
        '-'*15,
        ''])
    try:
        fp.write('intercept='+str(clf.intercept_)+'\n')
    except:
        pass
    if clftype in ['LogisticRegression', 'SGDClassifier', 'SVC', 'NuSVC', 'LinearSVC','MultinomialNB','GaussianNB']:
        if clftype in ['SVC', 'NuSVC']:
            if clf.get_params()['kernel']!='linear':
                fp.write('FEATURES\n')
                for i in a:
                    fp.write(i+'\n')
                fp.write('DUAL COEF\n')
                for i in clf.dual_coef_:
                    fp.write(str(i))
                fp.close()
                return
        n=len(list(col[1] for col in b))
        if clftype in ['LogisticRegression','SGDClassifier','MultinomialNB','GaussianNB']:
            names=list(str(i) for i in clf.classes_)
        elif (clftype in ['SVC','NuSVC']) and (clf.get_params()['kernel']=='linear'):
            names=list(str(i) for i in clf.classes_)
        elif clftype=='LinearSVC':
            l=clf.classes_
            names=list(str(l[i])+' vs '+str(l[j]) 
                for i in range(len(l)) 
                for j in range(len(l)) if l[i]<l[j] )
        
        #write all coefs
        fp.write('feature'.ljust(25)+''.join(name.ljust(25) for name in names)+'\n')
        for i in range(len(a)):
            fp.write(str(a[i]).ljust(25))
            for va in list(col[i] for col in b):
                fp.write(str(va).ljust(25))
            fp.write('\n')
        fp.write('\n')
        
        #write sorted coef for every class
        for i in range(n):
            fp.write('clf number='+str(i)+'\n')
            fp.write('-'*15+'\n')
            fp.write('sorted-feature'.ljust(25)+'class = '+names[i]+'\n')
            sorted_tuple=reversed(sorted(zip(a,b[i]),key=lambda x:x[1]))
            for va in sorted_tuple:
                fp.write(va[0].ljust(25)+str(va[1])+'\n')
            fp.write('\n')
        
    if clftype in ['DecisionTreeClassifier' ,'RandomForestClassifier']:
        fp.write('DT model\n')
        sorted_tuple=reversed(sorted(zip(a,b),key=lambda x:x[1]))
        for va in sorted_tuple:
            fp.write(va[0].ljust(25)+str(va[1])+'\n')
        fp.write('\n')

    if (clftype=='AdaBoostClassifier'):
        fp.write('ADa model\n')
        fp.write('NoTODO\n')
        
    if (clftype=='BaggingClassifier'):
        fp.write('Bag model\n')
        fp.write('NoTODO\n')


    
    fp.close()
    '''
    #write pdf for DT
    if clftype=='DecisionTreeClassifier':
        dot_data = StringIO()
        tree.export_graphviz(clf, out_file=dot_data)
        graph = pydot.graph_from_dot_data(dot_data.getvalue())
        graph.write_pdf(result['report_path']+"/tree.pdf")
    '''

    return True

