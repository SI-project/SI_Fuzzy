from string import punctuation
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer

def tokenize(text):
    return word_tokenize(text)

def lowercase(token_list):
    return [w.lower() for w in token_list]

def punctuations(token_list):
    return [w for w in token_list if w not in punctuation]

def stopWords(language, token_list):
    stop_words = set(stopwords.words(language))
    return [w for w in token_list if w not in stop_words]


def numbers(token_list):
    return [w for w in token_list if not w.isdigit()]

def stemming(token_list):
    ps = PorterStemmer()
    return list(set([ps.stem(w) for w in token_list]))

def stemming_no_contraction(token_list):
    ps = PorterStemmer()
    return [ps.stem(w) for  w in token_list]

def lemmatizing(token_list):
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(w) for w in token_list]

def allPreprocess(text,contract=True):
    tokens = tokenize(text)
    tokens = lowercase(tokens)
    tokens = punctuations(tokens)
    tokens = numbers(tokens)
    tokens = stopWords("english", tokens)
    if contract:
        tokens = stemming(tokens)
    else: tokens = stemming_no_contraction(tokens)
    tokens = lemmatizing(tokens)
    return tokens

def queryProcess(tokens):
    # tokens = [text]
    tokens = lowercase(tokens)
    tokens = stemming(tokens)
    tokens = lemmatizing(tokens)
    return "|".join(tokens)

def lower_stemming(word):
    token = [word]
    token = lowercase(token)
    token = stemming(token)
    return token[0]