from flask import Flask, request, session,g,redirect,url_for,abort,render_template,flash
from utils import *
from forms import SearchQueryData
import os
from search_controller import *
# CONFIGURATION

DEBUG = True
SECRET_KEY = 'development key'
UPLOAD_FILES_PATH = f'{os.getcwd()}/temp/files'

app = Flask(__name__)
app.config.from_object(__name__)
# app.config.from_envvar('MRIFUZZY_SETTINGS', silent=True)

def _get_results(query,files):

    name = 'Nombre del resultado'
    url = 'Url o path del resultado'
    description = "lorem impsum agsgasgasg\n asgasg asgasg asdf as asf asdf"
    result_info = GeneralResultInfo(10,1.0)
    return [ResultObject(name,url,description) for i in range(10)], result_info

@app.route('/',methods=['GET','POST'])
def show_entries():
    query = SearchQueryData(request.form)
    results = []
    result_info = GeneralResultInfo(0, 0.0)
    if request.method == "POST" and query.validate():
        print('Se hizo un post')
        query = SearchQueryData(request.form)
        results, result_info = get_results(query.query.data,query.folder_path.data)
        print(results)
        results = [ResultObject(result[1],''.join([query.folder_path.data,'/',result[1]]),result[0])for result in results]
    elif request.method == 'GET':
        print('se hizo un get')
    return render_template('show_entries.html',
                           results=results,
                           result_info=result_info,
                           query_form=query)


if __name__ == '__main__':
    app.run()
