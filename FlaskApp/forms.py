from wtforms import Form, TextField
from wtforms.fields.core import StringField
from wtforms import validators
from os.path import isdir
from fuzzy_model.parse_query import Parser
from fuzzy_model.lexer_query import Lexer

def validate_folder(form,field):
    if not isdir(field.data):
        raise validators.ValidationError("La carpeta no existe!")
def validate_query(form,field):
    l = Lexer()
    p = Parser(l)
    q = p.parse(field.data)
    if q is None:
        raise validators.ValidationError('La query no es válida!')

class SearchQueryData(Form):
    query = TextField('Query String',
                      [
                          validators.InputRequired('Se requiere una query!'),
                          validate_query
                      ])
    folder_path = StringField('Folder path',[
        validators.InputRequired('Se requiere de una carpeta!'),
        validate_folder
    ])
