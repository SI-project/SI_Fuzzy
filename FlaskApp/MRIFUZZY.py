from flask import Flask, request, session,g,redirect,url_for,abort,render_template,flash
import utils
from forms import SearchQueryData
# CONFIGURATION
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin@fuzzy.com'
PASSWORD = 'default'


app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('MRIFUZZY_SETTINGS', silent=True)

def _get_results(query):
    name = 'Nombre del resultado'
    url = 'Url o path del resultado'
    description = "lorem impsum agsgasgasg\n asgasg asgasg asdf as asf asdf"
    result_info = utils.GeneralResultInfo(10,1.0)
    return [utils.ResultObject(name,url,description) for i in range(10)], result_info

@app.route('/',methods=['GET','POST'])
def show_entries():

    if request.method == 'POST':
        query = SearchQueryData(request.form)
        searching = True
        results, result_info = _get_results(query)
    else:
        query = SearchQueryData()
        searching = False
        results = []
        result_info = utils.GeneralResultInfo(0, 0.0)
    return render_template('show_entries.html',
                           searching=searching,
                           results=results,
                           result_info=result_info,
                           query_form=query)

@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == "POST":
        print(app.config)
        if request.form['username'] != app.config["USERNAME"]:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html',error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run()
