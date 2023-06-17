import sys
from flask import Flask, render_template, request, redirect, url_for, session
from table_detection import ocr_image, filter_dataframe
import json


app=Flask(__name__)
app.config["SECRET_KEY"] = "kinmin_apps_co"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"


@app.route('/results', methods=['GET', 'POST'])
def results():
   return render_template('result.html')


@app.route('/', methods=['GET', 'POST'])
def upload():
   if request.method == 'POST':
       if request.files:
           file = request.files["file"]
           json_data = ocr_image(file)
           return redirect(url_for('results'))
   return render_template('index.html')

# @app.route('/at_work')
# def work_page():  
#    return render_template('output.html')

if __name__=='__main__':
    app.run(debug=True)