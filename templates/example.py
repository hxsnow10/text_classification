#encoding=utf-8

'''
textclf is our package.use help().
'''
from textclf.model import Train,Predict,Preprocess,TrainP,Debug
'''
packs inside import many sklearn functions.
'''
from textclf.model.packs import *
'''
tmodel定义为skleanr中grid_search(steps)组件，steps=pipeline(ext+sel+clf)。
这里是定死。如果想用其他模型，
常见的函数选项参见main_key_values
'''

ext=TfidfVectorizer()
sel=SelectKBest()
clf=LogisticRegression()

pipe=Pipeline([
    ('ext',ext),
	('sel',sel),
	('clf',clf)
    ])
#______________________________template中用户定义参数部分__________
#主要包括param_grid与下面函数的参数

#所有这里的参数可以多选进行模型选择
#单选即确定
#不选保持默认（不要让[]为空)
param_grid={
    'ext__binary':[False],#False:频度 True:频度归1
    "ext__ngram_range":[(1,1)],#ngram
    "ext__use_idf":[True],#True:TFIDF False:Vectorizer
    "sel__k":[20]#特征个数
    }

tmodel=GridSearchCV(pipe,param_grid,n_jobs=1,cv=3,verbose=10)#cv控制交叉验证的分割数

TrainT(
    tmodel=tmodel,#设置为定义好的tmodel
    data_path='data',#训练集路径
    report_path='report',#报告目录位置,
    pfrac=0.1,#测试集的比例
    debug_params={"samples":100}#debug的参数，samples表示提取出测试集中标注进行debug的个数
    )

#template为了方便使用，不管是skleanrn本身函数还是textclf的函数，隐藏了许多参数。
#templates基本是可用了。但是有时候超出了需求，请仔细查阅textclf文档与skleanrn文档。
