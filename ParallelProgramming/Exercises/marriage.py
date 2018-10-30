import random
import itertools
import math
import numpy
SIZE = 50
proposal_index = [0 for x in range(SIZE)]

def init_data():
    men = [list(numpy.random.permutation(list(range(SIZE)))) for _ in range(SIZE)]
    women = [list(numpy.random.permutation(list(range(SIZE)))) for _ in range(SIZE)]

    m_status = [-1 for _ in range(SIZE)]
    w_status = [-1 for _ in range(SIZE)]
    return men, women, m_status, w_status

def find_wife(m_pref, w_pref, m_status, w_status):
    proposals = list(range(SIZE))
    for man in range(SIZE):
        if(m_status[man] != -1):
            proposals[man] = -1
        else:
            print(SIZE-1-proposal_index[man])
            proposals[man] = m_pref[man].index(SIZE-1-proposal_index[man])
            proposal_index[man] = proposal_index[man] + 1
    return proposals

def propose(m_pref, w_pref, m_status, w_status, man, woman):
    if(woman == -1):
        return
    if(w_status[woman] == -1):
        w_status[woman] = man
        m_status[man] = woman
    elif(w_pref[woman][man] > w_pref[woman][w_status[woman]]):
        m_status[w_status[woman]] = -1
        w_status[woman] = man
        m_status[man] = woman


def manage_proposals(m_pref, w_pref, m_status, w_status, proposals):
    for man in range(SIZE):
        propose(m_pref, w_pref, m_status, w_status, man, proposals[man])


def check(m_status, w_status, m_pref, w_pref):
    for i in range(SIZE):
        if w_status[m_status[i]] != i:
            print("Incorrect match")
            return False 
        for j in range(SIZE):
            if i != j:                  # M1W1 M2W2   
                M1 = i
                M2 = j
                W1 = m_status[i]
                W2 = m_status[j]
                if w_pref[W2][M1] > w_pref[W2][M2] and m_pref[M1][W2] > m_pref[M1][W1]:
                    print("Woman", W2, "and man", M1, "prefer each other over their spouses")
                    print(M1, W1, M2, W2)
                    print(w_pref[W2])
                    print(m_pref[M1])
                    return False
                if w_pref[W1][M2] > w_pref[W1][M1] and m_pref[M2][W1] > m_pref[M2][W2]:
                    print("Woman", W1, "and man", M2, "prefer each other over their spouses")
                    print(M1, W1, M2, W2)
                    print(w_pref[W1])
                    print(m_pref[M2])
                    return False
    return True

m_pref, w_pref, m_status, w_status = init_data()

while(min(m_status) == -1):
    proposals = find_wife(m_pref, w_pref, m_status, w_status)
    manage_proposals(m_pref, w_pref, m_status, w_status, proposals)

print(m_status)
print(w_status)
print(m_pref)
print(w_pref)
print("Calculation complete, result is", "correct" if check(m_status, w_status, m_pref, w_pref) else "incorrect")