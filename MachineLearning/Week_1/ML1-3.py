D = {}

def ex3_1():
    for i in range(10):
        D[i] = str(i)

def ex3_2():
    d_iter = D.__iter__()
    for _ in range(5):
        print(d_iter.__next__())

def dGet(D, k):
    return any(k == x for x in D.keys())

def dGet2(D,k):
    return any(k is x for x in D.keys())

def dGet22(D,k):
    return len(list(filter(lambda x : x is k, D.keys()))) > 0