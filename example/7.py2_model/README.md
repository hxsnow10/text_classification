pylearn2 train process and predict
===============

1. balance data
$ #work like before

2. make_index_data
$ python makedata.py

3. train
$ train.py cnn.yaml

4. predict
$ python predict.py

5. deploy
$ python convert.py
  # convert to work in gpu-free enviroment
