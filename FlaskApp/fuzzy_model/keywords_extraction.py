from fuzzy_model.Fuzzy import term_fuzzy
from fuzzy_model.util import Zero_dict
from fuzzy_model.reader import Reader

def keyword_extraction(documents,path,k=20):
    r = Reader()
    documents = r.readDirectory(path,documents)
    word_relevance = Zero_dict()
    #input(documents)
    for doc in documents:
        for word in doc.keys():
            doc_relevance = term_fuzzy(word,doc,documents,path)  
            word_relevance[word]+= doc_relevance
    vocabulary = list(word_relevance.keys())
    k = min(k,len(vocabulary))
    most_relevant = sorted(vocabulary,key=lambda w: word_relevance[w],reverse=True)[:k]
    return most_relevant
            





