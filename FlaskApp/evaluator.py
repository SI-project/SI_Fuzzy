from fuzzy_model.Fuzzy import rank
from fuzzy_model.reader import Reader
from fuzzy_model.preprocess import allPreprocess
from fuzzy_model.lexer_query import Lexer
from fuzzy_model.parse_query import Parser
import fuzzy_model.feedback as feedback
from fuzzy_model.measures import accuracy,relay, f,f1
from random import choices
import json
#print(allPreprocess("Ant-Man"))
r = Reader()
directory = "./corpus/medicina"
r.readDirectory(directory)
print("documents are ready")
print(len(r.vocab))
l = Lexer()
p = Parser(l)
print("parser pass")

with open("./queries.txt") as fd:
    info = json.load(fd)
pres = []
recob = []

for i in range(len(info)):

    search = info[i]
    query = search["Text"]
    relevant_docs = search["RelevantDocuments"]
    print(query)
    query = p.parse(query)
    #print("Query #{}: {}".format(len(pres),query))
    #print("ranking {} documents".format(len(r.documents)))
    most_similar = rank(query,r.documents,directory)
    #print(most_similar)
    most_similar = [i[1] for i in filter(lambda doc: doc[0]>0.8,most_similar)]
    most_similar = [i[9:] for i in most_similar]
    #print(most_similar)
    print("finded {} results".format(len(most_similar)))
    rr = list(filter(lambda x: x in relevant_docs,most_similar))
    ri = list(filter(lambda x: not x in relevant_docs,most_similar))
    nr = list(filter(lambda x: not x in most_similar,relevant_docs))
    a = accuracy(rr,ri)
    rel = relay(rr,nr)
    pres.append(a)
    recob.append(rel)
    f_1 = f1(a,rel)
    f_2 = f(a,rel,2)
    f_05 = f(a,rel,0.5)
    print("P: {}, R:{}, F(1):{}, F(2):{}, F(0.5): {}".format(a,rel,f_1,f_2,f_05))
        

print(pres)
print(recob)


