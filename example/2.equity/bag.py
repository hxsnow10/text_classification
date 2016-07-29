#encoding=utf-8

from textclf.function import TrainT
from textclf.model.packs import *

ext=TfidfVectorizer()
sel=SelectKBest()
clf=BaggingClassifier()

pipe=Pipeline([
    ('ext',ext),
	('sel',sel),
	('clf',clf)
    ])
#----USER EDIT 1---------
param_grid={
    'ext__binary':[False]#False:频度 True:频度归1
    ,"ext__ngram_range":[(1,1)]#ngram
    ,"ext__use_idf":[True]#True:TFIDF False:Vectorizer
    ,"sel__k":[20]#特征个数
    ,"clf__base_estimator":[LogisticRegression()]#基础分类器
    
    #这里可以加上基础分类器的属性，例如
    #,"clf__base_estimator__n_iter":[100]
    
    ,"clf__n_estimators":[10]#分类器个数
    #,"max_samples":[0.5]#对于每个分类器选择的样例个数
    #,"max_features":[0.5]#对于每个分类器选择的特征个数
    }

tmodel=GridSearchCV(pipe,param_grid,n_jobs=1,cv=3,verbose=10)


TrainT(
    tmodel=tmodel,
    data_path='data',
    report_path='reportBAG',
    pfrac=0.1,
    debug_params={"samples":5}
    )

