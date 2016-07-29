import numpy

def load_weights(path, weights):
    inputfile = open(path,"rb")
    result = []
    for w in weights:
        result.append(  numpy.load(inputfile) )
    inputfile.close()
    return result

def save_weights(path, weights):
    outputfile = open(path,"wb")
    for w in weights:
        numpy.save(outputfile, w)
    outputfile.close()
