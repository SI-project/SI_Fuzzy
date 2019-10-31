from wtforms import Form, TextField
from wtforms.fields.core import StringField
from wtforms import validators
from os.path import isdir

def validate_folder(form,field):
    if not isdir(field.data):
        raise validators.ValidationError("La carpeta no existe!")

class SearchQueryData(Form):
    query = TextField('Query String',
                      [
                          validators.InputRequired('Se requiere una query!'),
                          # validators.Regexp(r'')
                      ])
    folder_path = StringField('Folder path',[
        validators.InputRequired('Se requiere de una carpeta!'),
        validate_folder
    ])
