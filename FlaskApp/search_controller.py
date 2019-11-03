from utils import GeneralResultInfo,ResultObject
import time
from fuzzy_model.Fuzzy import rank
from fuzzy_model.reader import Reader
from fuzzy_model.parse_query import Parser
from fuzzy_model.lexer_query import Lexer


def get_results(query,folder_path):
    r = Reader()
    r.readDirectory(folder_path)
    l = Lexer()
    p = Parser(l)
    query = p.parse(query)
    print("=========== {}".format(query))
    initial_time = time.time()
    most_similar = rank(query, r.documents)
    final_time = time.time() - initial_time
    result_info = GeneralResultInfo(len(most_similar), final_time)

    return most_similar, result_info