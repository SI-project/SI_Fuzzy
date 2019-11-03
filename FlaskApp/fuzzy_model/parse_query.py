import ply.yacc as yacc
from preprocess import queryProcess, lower_stemming
from lexer_query import Lexer
import json
class Parser(object):
    def __init__(self, lexer_instance):
        self.lexer = lexer_instance.lexer
        self.tokens = list(lexer_instance.tokens)

        with open("tesauro.json",'r') as fd:
            self.word_sinom = json.load(fd)
        self.parser = yacc.yacc(start='program', module=self)

    def parse(self, text):
        return self.parser.parse(text)

    def p_program(self, p):
        """
        program : query
        """
        p[0] = p[1]

    def p_query(self, p):
        """
        query : atom logic query
        """
        p[0] = p[1] + p[2] + p[3]

    def p_query_paren(self, p):
        """
        query : LPAREN query RPAREN
        """
        p[0] = p[1] + p[2] + p[3]

    def p_query_atom(self, p):
        """
        query : atom
        """
        p[0] = p[1]

    def p_atom_simple(self, p):
        """
        atom : term
        """
        p[0] = p[1]

    def p_atom_neg(self, p):
        """
        atom : NEG term
        """
        p[0] = p[1] + p[2]

    def p_term(self, p):
        """
        term : ID
        """
        w_modify = lower_stemming(p[1])
        sinom = self.word_sinom[w_modify] + [w_modify]
        word = queryProcess(sinom)
        p[0] = "({})".format(word)

    def p_logic(self, p):
        """
        logic : AND
              | OR
        """
        p[0] = p[1]

# l = Lexer()
# p = Parser(l)
# form = p.parse("blogs & test")
# print(form)