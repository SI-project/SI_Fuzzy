from wtforms import Form, TextField

class SearchQueryData(Form):
    query = TextField('Query String')