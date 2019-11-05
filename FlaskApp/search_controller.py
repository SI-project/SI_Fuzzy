from utils import GeneralResultInfo,ResultObject
import time
from fuzzy_model.Fuzzy import rank
from fuzzy_model.reader import Reader
from fuzzy_model.parse_query import Parser
from fuzzy_model.lexer_query import Lexer
from fuzzy_model.keywords_extraction import keyword_extraction


def get_results(query,folder_path):
    r = Reader()
    r.readDirectory(folder_path)
    l = Lexer()
    p = Parser(l)
    query = p.parse(query)
    print("=========== {}".format(query))
    initial_time = time.time()
    most_similar = rank(query, r.documents,folder_path)
    most_similar = list(filter(lambda x: x[0]>0.8,most_similar))
    final_time = time.time() - initial_time
    result_info = GeneralResultInfo(len(most_similar), final_time)

    return most_similar, result_info

def keywords(relevant,path):
    return keyword_extraction(relevant,path)
