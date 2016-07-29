#encoding=utf-8
from random import shuffle
def Balance_Data(data_path,new_data_path='data',balanced=0,balanced_num=None, random=1,homo=1,homo_frac=0.05):
    '''
    把数据转化成适合训练与测试的形式。
    
    parameters
    --------------
    data_path:数据路径
    new_data_path:结果数据路径(可以与data_path相同，但风险自己考虑)
    balanced：指把每个类别的数据个数都取一样 1:与最少看齐  2:设置数量
    random指把原本的顺序打乱
    homo指使每个类别均匀分布
    homo_frac指均匀分布的粒度
    '''
    fp=open(data_path,'r')
    lines=list(fp.readlines())
    fp.close()

    if random==1:
        shuffle(lines)
    
    class_lines={}
    for i in lines:
        s=i.split('\t')
        name=s[0]
        content=s[1]
        if name in class_lines:
            class_lines[name].append(i)
        else:
            class_lines[name]=[i]
    sum=len(lines)
    print '{0:15}{1:15}{2:15}'.format('class_name','numbers','frac')
    for i in class_lines:
        print '{0:15}{1:15}{2:15}'.format(i,len(class_lines[i]),len(class_lines[i])/sum)
    
    
    if balanced==1:
        num=min(list(len(class_lines[i]) for i in class_lines))
        for i in class_lines:
            class_lines[i]=extend(class_lines[i],num)
    elif balanced==2:
        if balanced_num!=None:
            num=balanced_num
        else:
            num=input('Enter Blanced Num')
        for i in class_lines:
            class_lines[i]=extend(class_lines[i],num)
    if balanced!=0:
        print 'after balanced:',len(class_lines)*num
    finallines=[]
    if homo==1:
        frac=homo_frac
        k=int(1/frac)
        for j in range(k):
            for i in class_lines:
                n=len(class_lines[i])
                finallines=finallines+class_lines[i][int(n*j*frac):int(n*(j+1)*frac)]
        lines=finallines
    print 'after homo 均匀化:',len(lines) 
    
    data=open(new_data_path,'w')
    for i in lines:
        data.write(i)
    data.close()

def extend(a,n):
    k=n/len(a)+1
    a=a*k
    return a[:n]
