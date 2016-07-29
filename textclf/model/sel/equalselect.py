#encoding=utf-8
from sklearn.base import BaseEstimator

class EqualSelect(BaseEstimator):
    def __init__(self,a=10):
        BaseEstimator.__init__(self)
        self.a=10
        self.supports=None
        pass

    def transform(self,X,y=None):
        return X

    def fit(self,X,y):
        self.supports=list(range(X.shape[1]))
        return self
 
    def get_support(self,indices=False):
        if indices==False:
            return len(self.supports)*[True,]
        else:
            return self.supports
