def ex2_1(lst):
    head, *tail = lst
    return head, tail

def ex2_2(lst):
    first = lst[0]
    last = lst[-1]
    return first+last, first-last, abs(first), int(last*last/last)

def ex2_3(lst):
    return sum(lst) # or from functools import reduce; reduce(lambda x,y:x+y, lst)

def ex2_4(lst):
    return lst[1::2]

def ex2_5(lst):
    return lst[:0:-1]

def ex2_6(lst):
    return lst[::-1]

def ex2_7(lst):
    return list(map(lambda x: x%2, lst))

lst = list(range(50))
print(ex2_1(lst))
print(ex2_2(lst))
print(ex2_3(lst))
print(ex2_4(lst))
print(ex2_5(lst))
print(ex2_6(lst))
print(ex2_7(lst))