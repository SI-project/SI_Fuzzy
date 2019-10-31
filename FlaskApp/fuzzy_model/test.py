from fuzzy_model.Fuzzy import rank
from fuzzy_model.reader import Reader
from fuzzy_model.preprocess import allPreprocess
from fuzzy_model.lexer_query import Lexer
from fuzzy_model.parse_query import Parser

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
