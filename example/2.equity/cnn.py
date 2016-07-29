#encoding=utf-8
#not supported

from textclf.function import *
from textclf.model.packs import *

ext=W2cTensor()
sel=EqualSelect()
clf=Cnn1()

pipe=Pipeline([
    ('ext',ext),
	('sel',sel),
	('clf',clf)
    ])

tmodel=pipe
#----------------------------
TrainT(
    nn=1,
    tmodel=tmodel,
    data_path='data',#训练集路径
    report_path='reportnn',#报告目录位置，注意不要重复，会自动覆盖
    pfrac=0.2,
    debug_params={"samples":0}
    )

    


