#encoding=utf-8

from textclf.function import TrainT
from textclf.model.packs import *

ext=TfidfVectorizer()
sel=SelectKBest()
clf=DecisionTreeClassifier()

pipe=Pipeline([
    ('ext',ext),
	('sel',sel),
	('clf',clf)
    ])
#----USER EDIT 1---------
param={
    'ext__binary':[False]#False:频度 True:频度归1
    ,"ext__ngram_range":[(1,1)]#ngram
    ,"ext__use_idf":[True]#True:TFIDF False:Vectorizer
    ,"sel__k":[20]#特征个数
    ,"clf__max_features":[None]#寻找最优分裂时寻找特征的个数，None表示sqrt(max_n)
    ,"clf__max_depth":[None]#树的最大深度，None表示直到叶子是纯洁的；控制clf__max_depth避免欠拟合与过拟合。
    #,"clf__min_samples_split":[]#分裂时samples最少需要多少个：
    #,"clf__min_samples_leaf":[]#成为一个叶子最少需要多少smaple:太小会导致过拟合
    }

tmodel=GridSearchCV(pipe,param,n_jobs=1,cv=3,verbose=10)

TrainT(
    tmodel=tmodel,
    data_path='data',#训练集路径
    report_path='reportDT',#报告目录位置
    pfrac=0.1,
    debug_params={'samples':5}
    )

