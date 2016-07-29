#encoding=utf-8
#not supported

from textclf.function import TrainT
from textclf.model.packs import *

ext=W2cTensor()
sel=EqualSelect()
clf=Cnn1()

pipe=Pipeline([
    ('ext',ext),
	('sel',sel),
	('clf',clf)
    ])

param_grid={
    'ext__binary':[False],#False:频度 True:频度归1
    "ext__ngram_range":[(1,1)],#ngram
    "ext__use_idf":[True],#True:TFIDF False:Vectorizer
    "sel__k":[20]#特征个数
    }

tmodel=GridSearchCV(pipe,param_grid,n_jobs=1,cv=3,verbose=10)#cv 控制cross_valition的数量
#----------------------------
TrainT(
    tmodel=tmodel,
    data_path='data',#训练集路径
    report_path='reportLR',#报告目录位置，注意不要重复，会自动覆盖
    pfrac=0.1,#测试集的比例
    debug_params={"samples":5}#debug的数量：对错误的测试结果输出debug信息
    )




