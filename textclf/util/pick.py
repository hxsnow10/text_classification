try:
    import Cpickle as pk
except:
    import pickle as pk

def pload(path):
    fp=open(path,'rb')
    obj=pk.load(fp)
    fp.close()
    return obj

def pdump(path,obj):
    fp=open(path,'wb')
    pk.dump(obj,fp)
    fp.close()
