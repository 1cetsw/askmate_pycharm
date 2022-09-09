import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import send_from_directory
import data_handler


app = Flask(__name__, static_url_path='/static')
UPLOAD_FOLDER = 'static/upload_file'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
FILE = 'sample_data/question.csv'
latest_opened_question_id = 0
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET',"POST"])
@app.route('/list')
def route_list():
    user_question = data_handler.get_all_user_question(FILE)

    return render_template('list.html', user_question=user_question)
@app.route('/add')
def route_add():
   return render_template('add.html')
@app.route('/result',methods = ['POST', 'GET'])
def result():
   global FILE
   mylist = []
   if request.method == 'POST':
        result = request.form
        for value in result.values():
            mylist.append(value)
        mylist.append('-')
        data_handler.write_user_question(FILE, mylist)
        return render_template("result.html",result = result)
   else:
        return render_template('result.html')

@app.route('/update/<question_id>', methods = ['POST', 'GET'])
def route_edit(question_id):
    table = data_handler.get_all_user_question(FILE)
    result = {}
    if request.method == 'GET':
        for line in table:
            if line['id'] == question_id:
                result = line
        return render_template('update.html', result = result)

@app.route('/result_edit', methods=['POST', 'GET'])
def route_edit_result():
    mylist = []
    if request.method == 'POST':
       new_result = request.form
       for value in new_result.values():
           mylist.append(value)
       data_handler.change_user_question(FILE, mylist)
       return render_template('result_edit.html', result=new_result, mylist = mylist)
    else:
        return render_template('result_edit.html')

@app.route('/question/<question_id>')
def route_display_question(question_id):
    table = data_handler.get_all_user_question(FILE)
    result = {}
    if request.method == 'GET':
        for line in table:
            if line['id'] == question_id:
                result = line
        return render_template('question.html', result=result)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/upload/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)
@app.route('/index')
def index():
    return render_template('index.html')
if __name__ == "__main__":
    app.run(debug = True)
