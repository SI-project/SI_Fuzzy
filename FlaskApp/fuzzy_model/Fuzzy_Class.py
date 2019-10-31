from sympy.logic.boolalg import to_dnf
from copy import copy
from fuzzy_model.util import Zero_dict
class Fuzzy_Model:
    def __init__(self,documents):
        self.c_ij_ = {}
        self.documents = documents
        self.built_cij()
        print("Cij ")
    #entre 0 y 1
    def built_cij(self):
        ni = Zero_dict()
        nij = Zero_dict()
        for doc in self.documents:
            words = list(doc.keys())
            for i,word in enumerate(words):
                for j in range(i,len(words)):
                    ni[word] = ni[word]+1
                    
                    nij[(word,words[j])] = nij[(word,words[j])]+ 1
                    nij[(words[j],word)] = nij[(words[j],word)]+ 1
        for i,j in nij.keys():
            old = nij[(i,j)]
            nij[(i,j)] = old/(ni[i]+ni[j]-old)
        self.c_ij_ = nij                    


    def c_ij(self,i,j):
        value = self.c_ij_[(i,j)]
        if value > 1: raise Exception("i: {} j:{}".format(i,j))
        return value
    #entre 0 y 1
    def term_fuzzy(self,term,doc):
        product = 1
        for word in doc.keys():
            if doc[word] == 1:
                product *= (1 - self.c_ij(term,word))
        return 1 - product


    def get_terms(self,Query,neg=True):
        splits = ["|"," ","&","(",")"]
        if neg: splits.append("~")
        for i in splits:
            Query = Query.replace(i," ")
        return Query.split()
    #entre 0 y 1
    def rank_cc(self,cc,Q_t,d_index):
        query_product = 1
        x =self.get_fdnf(self.get_terms(cc,False),Q_t,0)
        for component in x:
            fdnf_product = 1
            for term in component:
                if term[0] == "~":
                    fdnf_product*= (1 - self.term_fuzzy(term[1:],self.documents[d_index]))
                else:
                    fdnf_product*= self.term_fuzzy(term,self.documents[d_index])
            query_product*= (1 - fdnf_product)
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
    def rank_Cdnf(self,Query,d_index):
        Q_t = self.get_terms(Query)
        Q = str(to_dnf(Query,simplify=True))
        Q = Q.split("|")
        product = 1
        for cc in Q:
            product*= self.rank_cc(cc,Q_t,d_index)
        return 1 - product

    def rank(self,Query):
        ranks = []
        for i,_ in enumerate(self.documents):
            ranks.append(self.rank_Cdnf(Query,i))
        return sorted([(ranks[i],d.name) for i,d in enumerate(self.documents)],key=lambda x: x[0],reverse=True)


def rank(Query,documents):
    F = Fuzzy_Model(documents)
    return F.rank(Query)
# a ="A & (C | ~D)"
# documents = [{"A": 0, "B":0, "C":1, "D": 0},
#             {"A": 1, "B":1, "C":1, "D": 0},
#             {"A": 1, "B":0, "C":0, "D": 1}           
#             ]
# b = rank_Cdnf(a,documents,0)
# print(b)
# print(get_fdnf(get_terms("A",False),["A","D","C"], 0))

