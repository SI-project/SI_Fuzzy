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
app.config.from_envvar('MRIFUZZY_SETTINGS', silent=True)

def _get_results(query,files):

    name = 'Nombre del resultado'
    url = 'Url o path del resultado'
    description = "lorem impsum agsgasgasg\n asgasg asgasg asdf as asf asdf"
    result_info = GeneralResultInfo(10,1.0)
    return [ResultObject(name,url,description) for i in range(10)], result_info

@app.route('/upload-folder', methods=['POST'])
def upload_folder():
    files = request.files.getlist('file')
    id = 'empty'
    folder_name = ""
    folder_path=""
    uploaded = len(request.files)>0
    if request.files:
        folder_name = files[0].filename.split('/')[0]
        print(os.getcwd())
        id = hash(tuple(files))
        folder_path = f"{app.config['UPLOAD_FILES_PATH']}/{id}/{folder_name}"
        os.makedirs(folder_path,exist_ok=True)
        files = [file for file in files if file.filename.split('/')[-1].endswith('.txt') or file.filename.split('/')[-1].endswith('.pdf')]

        for file in files:
            file_name = file.filename.split('/')[-1]
            file_path = f"{folder_path}/{file_name}"
            file.save(file_path)
            print('saved '+ file_name)

    query = SearchQueryData()
    result_info = GeneralResultInfo(0, 0.0)
    form_path_param = folder_path.replace('/', '@')
    uploaded_folder_info = UploaddedFolderInfo(folder_name,len(files),form_path_param)
    return render_template('show_entries.html',
                           searching=False,
                           results=[],
                           result_info=result_info,
                           query_form=query,
                           uploaded_folder=uploaded,
                           uploaded_folder_info = uploaded_folder_info
                           )

@app.route('/search/folder<name>',methods=['POST'])
def search_call(name=""):
    name = name.replace("@",'/')
    query = SearchQueryData(request.form)
    searching = True
    results, result_info = get_results(query.query.data, name)

    return render_template('show_entries.html',
                           searching=searching,
                           results=results,
                           result_info=result_info,
                           query_form=query,
                           uploaded_folder=False)

@app.route('/',methods=['GET'])
def show_entries():

    query = SearchQueryData()
    searching = False
    results = []
    result_info = GeneralResultInfo(0, 0.0)
    return render_template('show_entries.html',
                           searching=searching,
                           results=results,
                           result_info=result_info,
                           query_form=query,
                           uploaded_folder=False)


if __name__ == '__main__':
    app.run()
