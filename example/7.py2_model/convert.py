#make sure ~/.theanorc  device=cpu
import os
import sys
from pylearn2.config import yaml_parse

os.environ['THEANO_FLAGS']="device=cpu"
 
from pylearn2.utils import serial
 
in_path = sys.argv[1]
model = serial.load(in_path)
 
model2 = yaml_parse.load(model.yaml_src)
model2.set_param_values(model.get_param_values())
 
out_path = sys.argv[2]
serial.save(out_path, model2)
