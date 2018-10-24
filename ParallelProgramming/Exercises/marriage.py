import random
import itertools
import math
import numpy
SIZE = 2

def init_data():
    men = []
    women = []
    for _ in range(SIZE):
        a = numpy.random.permutation(list(range(SIZE)))
        men.append(list(a))
    for _ in range(SIZE):
        a = numpy.random.permutation(list(range(SIZE)))
        women.append(list(a))

    m_status = []
    w_status = []
    for _ in range(SIZE):
        m_status.append(-1)
        w_status.append(-1)
    return men, women, m_status, w_status

def find_wife(man_idx, m_status, w_status, m_pref, w_pref):
    print("Man #", man_idx, "looking for wife")
    for i in range(SIZE-1, -1, -1):                         # iterate through each woman by preference until engaged
        choice = m_pref[man_idx].index(i)                   # asking this woman
        print("  Asking out woman #", choice)
        if w_status[choice] == -1:                          # she's available
            w_status[choice] = man_idx                      # engage woman to man
            m_status[man_idx] = choice                      # engage man to woman
            return
        elif w_pref[man_idx] > w_pref[w_status[choice]]:    # she likes this one more
            m_status[w_status[choice]] = -1                 # other man cri like baby
            w_status[choice] = man_idx                      # engage woman to man
            m_status[man_idx] = choice                      # engage man to woman
            return

def check(m_status, w_status, m_pref, w_pref):
    for i in range(SIZE):
        if w_status[m_status[i]] != i:
            return False 
        for j in range(SIZE):
            if i != j:                  # M1W1 M2W2   
                M1 = i
                M2 = j
                W1 = m_status[i]
                W2 = m_status[j]
                if w_pref[W2][M1] > w_pref[W2][M2] and m_pref[M1][W2] > m_pref[M1][W1]:
                    return False
                if w_pref[W1][M2] > w_pref[W1][M1] and m_pref[M2][W1] > m_pref[M2][W2]:
                    return False
    return True

m_pref, w_pref, m_status, w_status = init_data()

flag = True
while(flag):
    flag = False
    for i in range(SIZE):
        if m_status[i] == -1:                   # man lf woman
            flag = True                         # we stop when all men are engaged
            find_wife(i, m_status, w_status, m_pref, w_pref)
print(m_status)
print(w_status)
print(m_pref)
print(w_pref)
print("Calculation complete, result is", "correct" if check(m_status, w_status, m_pref, w_pref) else "incorrect")

