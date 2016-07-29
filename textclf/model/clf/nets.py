#encoding=utf-8
from pylearn2.train import Train

from sklearn.base import BaseEstimator
from sklearn.base import ClassifierMixin

class Nets():
    '''pylearn2 based network models.
    '''
    
    def __init__(model=None,train_params={}):
        self.model=model
        self.set_train_params(train_params)
        
    def set_train_params(train_params={}):
        for i in train_params:
            self.train_params[i]=train_params[i]

    def fit(X,y=None):#TODO
        dataset=
        self.set_train_params(train_params={
            'dtataset':dataset,
            'algorithm':algorithm,
            'extensions':extension})#which influenced by X,y
            #real data or symbol?
        train=Train(model=self.model,**self.train_params)
        train.main_loop()

    def transform(X):
        return self.model.fprop(X)

    def predict(X):
        return self.model.fprop(X)
        
