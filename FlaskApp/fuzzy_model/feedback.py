from fuzzy_model.util import *
from fuzzy_model.reader import Reader
import numpy as np
from fuzzy_model.preprocess import allPreprocess


def get_vocabulary(documents):
    vocabulary = set([])
    for doc in documents:
        vocabulary = vocabulary.union(doc)
    return list(vocabulary)

def tf_idf(documents,vocab):
    vocab_to_index = dict(zip(vocab,range(len(vocab))))
    tf = np.zeros((len(vocab),len(documents)))
    #df = np.zeros(len(vocab))
    for j,doc in enumerate(documents):
        for word in doc:
            i = vocab_to_index[word]
            tf[i,j] += 1
            #if tf[i,j] == 1:
            #    df[i] += 1
    #mx = tf.max(axis=0)
    #tf = (tf/mx)
    #tf_idf = (tf.transpose()*df/len(documents)).transpose()
    return tf

def process_docs(documents):
    return [allPreprocess(d,False) for d in documents]
        
def get_most_relevant_words(documents,random_space,keywords_per_doc = 100):
    vocab = get_vocabulary(documents+random_space)
    keywords_set = set(vocab)
    for i in range(len(documents)):
        n_docs = [documents[i]]+random_space
        tfidf =  tf_idf(n_docs,vocab)
        doc = get_column_vector(tfidf,0)
        keywords_set = keywords_set.intersection([vocab[i] for i in keywords(doc,keywords_per_doc)])
    return list(keywords_set)

def keywords(document,count):
    count = min(count,sum([1 for i in filter(lambda x: x>0.10,document)]))
    return sorted(range(len(document)),key=lambda x: document[x])[:count]

def get_documents(names,directory):
    R = Reader()
    docs = R.readDirectory(directory,names)
    return [d[1] for d in docs]

def get_keywords(results,directory,random_space,most_relevant=10):
    most_relevant = min(most_relevant,len(results))
    names = [r[1] for r in results][:most_relevant]
    documents = get_documents(names,directory)
    documents = process_docs(documents)
    names_r = [r[1] for r in random_space]
    random_space = get_documents(names_r,directory)
    random_space = process_docs(random_space)
    if most_relevant>0:
        keywords = get_most_relevant_words(documents,random_space)
        return keywords
    return []
def expand_query(query,results,directory,random_space):
    keywords = get_keywords(results,directory,random_space)
    if len(keywords) > 0:
        component = keywords[0]
        for i in range(1,len(keywords)):
            component += "&{}".format(keywords[i])
        query = "({}) | ({})".format(query,component)
    return query


#d1 = {"casa":1, "perro":1, "hogar":1}
#d2 = {"casa":1, "gato":1, "hogar":1}
#docs = [d1,d2]
#docs = ["the dog lives in the garden where scrapy is sleeping but no one butter drink cook cookie","my mother dog has cookie a dog"]

#keywords = get_most_relevant_words(docs)
#print(keywords)
#print(get_vocabulary([d1,d2]))