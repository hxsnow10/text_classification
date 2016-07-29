#encoding=utf-8

from textclf.function import TrainT

TrainT(
    data_path='new_data',
    report_path='new_report',
    model_params={
        'GridSearchCV.estimator':'Pipeline',
        'GridSearchCV.param_grid':{},
        'steps.ext':'CountVectorizer',
        'steps.sel':'SelectKBest',
        'steps.clf':'LogisticRegression',
        'SelectKBest.k':100
    },
    pfrac=0.1,
    debug_params={'samples':10}
    )
