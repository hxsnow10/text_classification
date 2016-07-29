#encodin=utf8
import readline

def checkouty(y,check=1):
    num={}
    for i in y:
        if i in num:
            num[i]=num[i]+1
        else:
            num[i]=1
    for i in num:
        print 'num',i,'=',num[i]
    if check==0:
        return 'y'
    else:
        return raw_input('GO On?(y/n)')

