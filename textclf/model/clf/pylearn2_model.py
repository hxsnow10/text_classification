#encoding=utf-8
from collections import OrderedDict
import theano
from theano import tensor as T
from theano import function

from textclf.model.pre import *
from textclf.util import *
from textclf.data import *

from pylearn2.utils import serial
from pylearn2.models.mlp import *

class Pylearn2_model():
    def __init__(self,model_path,enable_rule=False):
        model = pload(model_path)
        self.model=model
        self.model.layers[0].enable_rule=enable_rule
        self.model.redo_theano() 
        X = model.get_input_space().make_theano_batch()
        Y = model.fprop( X)
        Class = T.argmax( Y, axis = 1 )
        self.p = theano.function( [X], Class, allow_input_downcast=True)
        self.p_proba = theano.function( [X], Y, allow_input_downcast=True)

    def transform(self,X,proba=True):
        if not proba:
            return self.p(X)
        else:
            return self.p_proba(X)
            
    def predict_debug(self,X):
        return data_flow(self.model,X)

def data_flow(layer,state_blow):
    '''
    data_flow for mlp,composite
    
    return
    (name,Orderdict{data_flow(sub_layer)})
    '''
    name=layer.layer_name
    ltype=layer.__class__.__name__
    print name,ltype
    if ltype=='MLP':
        rval=OrderedDict()
        state=state_blow
        for sub_layer in layer.layers:
            state_blow=state
            sub_name,state,sub_rval=data_flow(sub_layer,state_blow)
            rval[sub_name]=sub_rval
    elif ltype=='CompositeLayer':
        rval=OrderedDict()
        state=[]
        for sub_layer in layer.layers:
            sub_name,sub_state,sub_rval=data_flow(sub_layer,state_blow)
            rval[sub_name]=sub_rval
            state.append(sub_state)#TODO 这里只考虑了全映射的情况
    elif ltype=='ConvElemwise' or 'ConvRectifiedLinear':
        '''
        input---->conv_layer---->pooling
        这里的问题是可能需要把conv_layer也显示出来，可以在ltype 类中加2个方法，返回conv 与 pool 算子。先不实现
        '''
        state=compute(layer.fprop,state_blow)
        rval=state
    elif ltype=='W2v':
        state=compute(layer.fprop,state_blow,'int32')
        rval=state
    else:
        state=compute(layer.fprop,state_blow)
        rval=state
    
    return name,state,rval

def compute(fprop,state_blow,dtype='float32'):
    X=theano.shared(value=state_blow,type=dtype)
    y=fprop(X)
    print 'got ',y.eval()
    return y.eval()
