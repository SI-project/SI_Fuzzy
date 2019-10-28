from fuzzy import rank
from reader import Reader
from preprocess import allPreprocess
from lexer_query import Lexer
from parse_query import Parser

#print(allPreprocess("Ant-Man"))
r = Reader()
r.readDirectory("./")
query = "iron & azaceta"
l = Lexer()
p = Parser(l)

# query = allPreprocess(query)
query = p.parse(query)
print(query)
most_similar = rank(query,r.documents)
print(most_similar)
