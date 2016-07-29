#encoding=utf-8

from textclf.function import TrainT
from textclf.model.packs import *

ext=TfidfVectorizer()
sel=SelectKBest()
clf=SGDClassifier()

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
    ,"sel__k":[2000]#特征个数
    ,"clf__loss":['hinge']#损失函数
    ,"clf__n_iter":[30]#循环的次数
    }

tmodel=GridSearchCV(pipe,param_grid,n_jobs=1,cv=3,verbose=10)

TrainT(
    tmodel=tmodel,
    data_path='data',#训练集路径
    report_path='report_SGD_SVC',#报告目录位置
    pfrac=0.1,
    debug_params={"samples":5}
    )

