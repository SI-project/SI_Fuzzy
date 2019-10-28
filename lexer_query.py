import ply.lex as lex
from ply.lex import TOKEN

class Lexer(object):
    def __init__(self):
        self.reserved = ()
        self.tokens = self.tokens_list
        self.lexer = lex.lex(module=self)

    def test(self, text):
        self.lexer.input(text)
        while True:
            token = self.lexer.token()
            if not token:
                break
            print(token)

    t_ignore = ' \t\r\f'

    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_AND = r'\&'
    t_OR = r'\|'
    t_NEG = r'\~'
    t_ID = r'[a-zA-Z]+'

    @property
    def tokens_list(self):
        return (
            'LPAREN', 'RPAREN', 'AND', 'OR', 'NEG', 'ID'
        )

# L = Lexer()
# L.test("iron & man&~Spider")