#encoding=utf-8
from textclf.data.get_raw import *
from textclf.model.packs import *

def Predict(model_path,data_path,raw_params={},withpre=1,pre_params={'type':'label'}):
    raw_X,raw_y=get_raw(data_path,dtype='path',raw_params=raw_params)
    moodel=pload(model_path)
    if withpre==1:
        pre_y=model.predict(raw_X)
    else:
        X=Preprocess(**pre_params).transform(raw_X)
        pre_y=model.predict(X)
    fp=open('y','w')
    for i in pre_y:
        fp.write(str(i)+'\n')
    fp.close()

'''大致逻辑如此, function里有一个predict函数
pickle.load(model)
X=pre.transform(X)#if nopre_model should pre first
y=model.predict(X)
'''

'''如果要消除依赖，在无textclf的地方部署预测
使用nopre的模型，先提取内容预处理然后 model.predict(X) 或者model.predict([content])[0]
'''

