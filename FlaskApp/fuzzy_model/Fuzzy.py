from sympy import to_dnf
from copy import copy
import pickle

def dot(x,y):
    x*= 1000
    y*=1000
    return (x*y)/1000000

def rest(x,y):
    x*=1000
    y*=1000
    return (x-y)/1000

class fuzzy_logic:
    def __init__(self):
        self.CIJ = {}
#entre 0 y 1
    def c_ij(self,i,j,documents):
        try:
            return self.CIJ[(i,j)]
        except:
            return self.cij(i,j,documents)
        
    def cij(self,i,j,documents):
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
        value = round(value,3)
        self.CIJ[(i,j)] = value
        self.CIJ[(j,i)] = value
        if value > 1: raise Exception("i: {} j:{}, ni : {},nj: {},nij: {}".format(i,j,ni, nj, nij))
        return value

    #entre 0 y 1
    def term_fuzzy(self,term,doc,documents):
        product = 1
        for word in doc.keys():
            if doc[word] == 1:
                product = dot(rest(1, self.c_ij(term,word,documents)),product)
                product = round(product,3)
        return rest(1,product)


    def get_terms(self,Query,neg=True):
        splits = ["|"," ","&","(",")"]
        if neg: splits.append("~")
        for i in splits:
            Query = Query.replace(i," ")
        return Query.split()
    #entre 0 y 1
    def rank_cc(self,cc,documents,Q_t,d_index):
        query_product = 1
        x =self.get_fdnf(self.get_terms(cc,False),Q_t,0)
        for component in x:
            fdnf_product = 1
            for term in component:
                if term[0] == "~":
                    fdnf_product= dot(rest(1,self.term_fuzzy(term[1:],documents[d_index],documents)),fdnf_product)
                    
                else:
                    fdnf_product = dot(self.term_fuzzy(term,documents[d_index],documents),fdnf_product)
                fdnf_product = round(fdnf_product,3)
            query_product = dot(rest(1, fdnf_product),query_product)
            query_product = round(query_product,3)
        return query_product


    def get_fdnf(self,cc,Q_t,index):
        if index == len(Q_t): return [copy(cc)]
        term = Q_t[index]
        neg_t = "~"+term
        if neg_t in cc or term in cc:
            return self.get_fdnf(cc,Q_t,index+1)
        else:
            cc.append(neg_t)
            l = self.get_fdnf(cc,Q_t,index+1)
            cc.pop()
            cc.append(term)
            r= l + self.get_fdnf(cc,Q_t,index+1)
            cc.pop()
            return r
        

    #entre 0 y 1
    def rank_Cdnf(self,Query,documents,d_index):
        Q_t = self.get_terms(Query)
        Q = str(to_dnf(Query,simplify=True))
        Q = Q.split("|")
        product = 1
        
        for cc in Q:
            product = dot(self.rank_cc(cc,documents,Q_t,d_index),product)
            product = round(product,3)
        return rest(1,product)

    def rank(self,Query,documents):
        ranks = []
        for i,_ in enumerate(documents):
            ranks.append(self.rank_Cdnf(Query,documents,i))
        return sorted([(ranks[i],d.name) for i,d in enumerate(documents)],key=lambda x: x[0],reverse=True)

def rank(Qery,documents,path):
    try:
        with open(path+"/"+"fuzzy.pickle") as fd:
            ranker = pickle.load(fd)
    except:
        ranker = fuzzy_logic()
    rnk = ranker.rank(Qery,documents)
    with open(path+"/"+"fuzzy.pickle","wb+") as fd:
        pickle.dump(ranker,fd)
    return rnk
def term_fuzzy(term,doc,documents,path):
    try:
        with open(path+"/"+"fuzzy.pickle") as fd:
            ranker = pickle.load(fd)
    except:
        ranker = fuzzy_logic()
    return ranker.term_fuzzy(term,doc,documents)

# a ="A & (C | ~D)"
# documents = [{"A": 0, "B":0, "C":1, "D": 0},
#             {"A": 1, "B":1, "C":1, "D": 0},
#             {"A": 1, "B":0, "C":0, "D": 1}           
#             ]
# b = rank_Cdnf(a,documents,0)
# print(b)
# print(get_fdnf(get_terms("A",False),["A","D","C"], 0))