#coding=utf-8

def get_raw(data,dtype='path',raw_params={}):
    '''
    get X(documentation vector) y(label vector) from data using rawer.
    rawer is build from raw_params.
    if rawer is for unlabel, y=[].
    '''

    rawer=build_raw(**raw_params)
    if dtype=='line':
        lines=[data]
    else:
        fp = open(data, "r")
        lines=fp.readlines()
        print len(lines)
        fp.close()
    raw_x,raw_y,error_line=[],[],[]
    for i in range(len(lines)):
        line=lines[i]
        s=rawer(line)
        if s==None:
            error_line.append(i)
            continue
        if 'x' in s:
            raw_x.append(s['x'])
        if 'y' in s:
            raw_y.append(s['y'])
    print 'illegal lines sum='+str(len(error_line))
    print 'illegal index=',
    for i in error_line:
        print i,
    print ''
    return raw_x,raw_y,error_line

def build_raw(type='label',raw=None):
    '''
    build rawer
    '''
    if type=='label':
        rawer=raw_label
    elif type=='unlabel':
        rawer=raw_unlabel
    elif type=='user':
        rawer=raw
    return rawer

def raw_label(line):
    item = line.strip().split('\t')
    s={}
    if len(item)<2:
        return None
    s['x']=' '.join(item[1:])
    s['y']=item[0]
    return s

def raw_unlabel(line):
    s={}
    if line=='\n':
        return None
    s['x']=line
    return s

class raw():
    def __init__(self,type='label'):
        self.type=type
        
    def transform(self,data_path):
        return get_raw(data=data_path)
        
