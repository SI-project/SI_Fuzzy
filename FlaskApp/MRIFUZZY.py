from flask import Flask, request,render_template_string, send_file,session,redirect,url_for,abort,send_from_directory,render_template,flash
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

@app.route('/getfile')
def getfile():
    path = request.args['path']
    print(path)
    path = path.replace('@','/')
    splited = path.split('/')
    name_file = splited[-1]
    name_directory = '/'.join([f'{i}/'for i in splited[:-1]])
    print(name_directory,name_file)
    return send_from_directory(name_directory,name_file)


@app.route('/retro',methods=['POST'])
def retro():
    checks = request.json['list']
    print('La lista de los checks: ',checks)
    return render_template_string('OK')


@app.route('/',methods=['GET','POST'])
def show_entries():
    query = SearchQueryData(request.form)
    results = []
    result_info = GeneralResultInfo(0, 0.0)
    initial = True
    if request.method == "POST" and query.validate():
        print('Se hizo un post')
        query = SearchQueryData(request.form)
        results, result_info = get_results(query.query.data,query.folder_path.data)
        print(results)
        results = [ResultObject(result[1],''.join([query.folder_path.data,'/',result[1]]).replace('/','@'),result[2], value=result[0])for result in results]
        initial = False
    return render_template('show_entries.html',
                           results=results,
                           result_info=result_info,
                           query_form=query,
                           initial=initial)


if __name__ == '__main__':
    app.run()
