from sympy.logic.boolalg import to_dnf
from copy import copy

#entre 0 y 1
def c_ij(i,j,documents):
    nij = 0
    ni = 0
    nj = 0
    for doc in documents:
        if doc[i] == 1:
            ni += 1
            if doc[j] == 1:
                nj+= 1
                nij+= 1
        elif doc[j] == 1:
            nj+= 1
    value = nij/(ni+nj-nij)
    if value > 1: raise Exception("i: {} j:{}, ni : {},nj: {},nij: {}".format(i,j,ni, nj, nij))
    return value

#entre 0 y 1
def term_fuzzy(term,doc,documents):
    product = 1
    for word in doc.keys():
        if doc[word] == 1:
            product *= (1 - c_ij(term,word,documents))
    return 1 - product


def get_terms(Query,neg=True):
    splits = ["|"," ","&","(",")"]
    if neg: splits.append("~")
    Q_l = Query
    for i in splits:
        Query = Query.replace(i," ")
    return Query.split()
#entre 0 y 1
def rank_cc(cc,documents,Q_t,d_index):
    query_product = 1
    x =get_fdnf(get_terms(cc,False),Q_t,0)
    for component in x:
        fdnf_product = 1
        for term in component:
            if term[0] == "~":
                fdnf_product*= (1 - term_fuzzy(term[1:],documents[d_index],documents))
            else:
                fdnf_product*= term_fuzzy(term,documents[d_index],documents)
        query_product*= (1 - fdnf_product)
    return query_product


def get_fdnf(cc,Q_t,index):
    if index == len(Q_t): return [copy(cc)]
    term = Q_t[index]
    neg_t = "~"+term
    if neg_t in cc or term in cc:
        return get_fdnf(cc,Q_t,index+1)
    else:
        cc.append(neg_t)
        l = get_fdnf(cc,Q_t,index+1)
        cc.pop()
        cc.append(term)
        r= l + get_fdnf(cc,Q_t,index+1)
        cc.pop()
        return r
    

#entre 0 y 1
def rank_Cdnf(Query,documents,d_index):
    Q_t = get_terms(Query)
    Q = str(to_dnf(Query,simplify=True))
    Q = Q.split("|")
    product = 1
    for cc in Q:
        product*= rank_cc(cc,documents,Q_t,d_index)
    return 1 - product

def rank(Query,documents):
    ranks = []
    for i,d in enumerate(documents):
        ranks.append(rank_Cdnf(Query,documents,i))
    return sorted([(ranks[i],d.name,d.description) for i,d in enumerate(documents)],key=lambda x: x[0],reverse=True)

# a ="A & (C | ~D)"
# documents = [{"A": 0, "B":0, "C":1, "D": 0},
#             {"A": 1, "B":1, "C":1, "D": 0},
#             {"A": 1, "B":0, "C":0, "D": 1}           
#             ]
# b = rank_Cdnf(a,documents,0)
# print(b)
# print(get_fdnf(get_terms("A",False),["A","D","C"], 0))