TEXT_CLASSFICATION
===============================
Offer text classification service.

说在前面
-----------
本框架并非立足于服务于小白，而是稳定地提供库-模型相关的一些函数与工程上的管理，减少工程上的重复劳动。
即不要期望不学习模型，不理解库函数(比如sklearn,pylearn)，而本框架会帮你包办性能问题。
反对机器学习工作者无脑复用别人的代码来完成任务，长期上极为不利。

然而这里做的工作有限，就是对常用代码的封装，新手可以通过阅读代码熟悉sklearn、pylearn2。请用你最适合的方式使用。


Introduction
-----------
We hope to offer convient and powerful tools for text calssification.  
It is a simple tool more than a complete toolbox or package.
We offer several(<=5) API for training model for classification based on sklearn and pylearn2.
TrainT for classic algorithms of sklearn, theano、pylearn2、blocks for deep learning.

I believe really freedom and powerful, not only about this field, should get by hacking and combining yourselves.
Here, at least you can get more power through sklearn, theano themselves ,whereas This tool is to reduce programming and considerating complicated(power) parameters.


Now State
-----------
* balance data.
* preprocess build.Preprocess transform raw text line (may with label) to (X,y).
* model build.Now we provide a model GridSearchCV(Pileline(steps=(('exc',),('sel',),('clf',))),...).Two types of model building is offered.
* Train, Test, Debug.
* Report. whether Train or Test, we give some report.
* deeplearning use theano code/pylearn2 straight.now only one pylearn2 yaml.


Vision State
-----------
We hope it develop a good code pool about all about text_classification.

Installation
-----------
copy textclf to ../site-packages
copy 1.58:/opt/xia.hong/pylearn2/pylearn2 to ../site-packages

Usage
-----------
> from textclf.function import TrainT  
  TrainT()#用这个就基本OK了  
  other api:Balance_Data,Train,Test,Debug,Deploy

> makedata & train.py cnn.yaml

refer to tutorial for details

Contact
-----------
xia.hong@baifemdian.com
