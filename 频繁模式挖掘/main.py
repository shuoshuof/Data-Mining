import math
min_sup = 2
def get_L(C_k,data):
    for key in C_k.keys():
        for item in data:
            if set(key).issubset(item):
                C_k[key]+=1
    for key in list(C_k.keys()):
        if C_k[key]<min_sup:
            del C_k[key]
            continue
    return C_k
def cut(C_k,L):
    C_k_1=dict()
    for key in C_k.keys():
        item = set(key)
        temp =0
        base = len(item)
        for key1,value1 in L.items():
            if set(key1).issubset(item):
                temp+=1
        if temp==math.factorial(base)/(math.factorial(1)*math.factorial(base-1)):
            C_k_1[key]=0
    return C_k_1
def get_Ck(L:dict):
    C_k = dict()
    for key in L.keys():
        for key1,value1 in L.items():
            new_item = set(key)|set(key1)
            if len(new_item)==len(key)+1:
                new_item = [str(i) for i in new_item]
                new_item.sort()
                new_item = ''.join(new_item)
                if new_item not in C_k:
                    C_k[new_item] =0
    return C_k
if __name__=='__main__':
    # data = [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]
    # data =[['A','C','D'],['B','C','E'],['A','B','C','E'],['B','E']]
    data =[[1,2,5], [2,4], [2,3], [1,2,4], [1,3], [2,3], [1,3], [1,2,3,5], [1,2,3]]

    C = dict()
    for item in data:
        for t in item:
            if str(t) in C:
                C[str(t)]+=1
            else:
                C[str(t)] = 1
    data1 = []
    for item in data:
        item1 = [str(t)for t in item]
        data1.append(set(item1))
    # print(data1)
    L={}
    for key,value in C.items():
        if value>=min_sup:
            L[key]=value
    # print(L)
    result = []
    result.append([{tuple(set(key)): L[key]}for key in L.keys()])
    while  len(L)>1:
        C_k=get_Ck(L)
        # print("连接:",C_k)
        C_k = cut(C_k,L)
        # print("剪枝后:",C_k)
        L = get_L(C_k,data1)
        # print(L)
        result.append([{tuple(set(key)): L[key]}for key in L.keys()])
    print(result)