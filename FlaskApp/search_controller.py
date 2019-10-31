from utils import GeneralResultInfo,ResultObject
import time
from fuzzy_model.Fuzzy import rank
from fuzzy_model.reader import Reader
from fuzzy_model.parse_query import Parser
from fuzzy_model.lexer_query import Lexer


def get_results(query,folder_path):
    r = Reader()
    r.readDirectory(folder_path)
    print(f"Analicemos la siguiente carpeta {folder_path}")
    l = Lexer()
    p = Parser(l)
    print(f'Los documentos cargados {r.documents}')
    query = p.parse(query)
    print(query)
    initial_time = time.time()
    most_similar = rank(query, r.documents)
    print(most_similar)
    final_time = time.time() - initial_time
    result_info = GeneralResultInfo(len(most_similar), final_time)

    return most_similar, result_info