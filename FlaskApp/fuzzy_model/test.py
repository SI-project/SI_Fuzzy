from Fuzzy import rank
from reader import Reader
from preprocess import allPreprocess
from lexer_query import Lexer
from parse_query import Parser
import feedback
from random import choices
#print(allPreprocess("Ant-Man"))
r = Reader()
r.readDirectory("./")
query = "blog & firearm"
l = Lexer()
p = Parser(l)

# query = allPreprocess(query)
query = p.parse(query)
print(query)
most_similar = rank(query,r.documents)
print(most_similar)

keys= feedback.get_keywords(most_similar,"./",choices(most_similar[30:],k=20))
print(keys)