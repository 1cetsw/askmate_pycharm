from flask import Flask, render_template, request, redirect, url_for

import data_handler
app = Flask(__name__)

FILE = 'question.csv'

@app.route("/")
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

if __name__ == "__main__":
    app.run()
