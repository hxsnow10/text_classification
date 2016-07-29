#encoding=utf-8

from textclf.function import TrainT
from textclf.model.packs import *

ext=TfidfVectorizer()
sel=SelectKBest()
clf=SVC()

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
    ,"clf__kernel":['rbf']#kernl 可以为'rbf' 'linear' 'poly'
    ,"clf__probability":[True]#如果希望模型可以预测概率即使用prod_***，必须定义为True
    ,"clf__max_iter":[30]#循环的次数
    #,"clf__C":[]
    #,"clf__degree":[]
    #,"clf__gamma":[]
    #,"clf__coef0":[]
    }

tmodel=GridSearchCV(pipe,param_grid,n_jobs=1,cv=3,verbose=10)

TrainT(
    tmodel=tmodel,
    data_path='data',#训练集路径
    report_path='reportSVC',#报告目录位置
    pfrac=0.1,
    debug_params={"samples":5}
    )

