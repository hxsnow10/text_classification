import numpy
def npy_load(path):
    inputfile = open(path,"rb")
    result=numpy.load(inputfile)
    inputfile.close()
    return result

def npy_save(path, weight):
    outputfile = open(path,"wb")
    numpy.save(outputfile, weight)
    outputfile.close()

def npy_loads(path, weights):
    inputfile = open(path,"rb")
    result = []
    for w in weights:
        result.append(numpy.load(inputfile))
    inputfile.close()
    return result

def npy_saves(path, weights):
    outputfile = open(path,"wb")
    for w in weights:
        numpy.save(outputfile, w)
    outputfile.close()

