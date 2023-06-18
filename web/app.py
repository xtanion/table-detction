from os.path import join, curdir
from flask import Flask, render_template, request, redirect, url_for, send_file, Response
from table_detection import crop_table, TEMP_DIR


app=Flask(__name__)
app.config["SECRET_KEY"] = "kinmin_apps_co"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"


@app.route('/results', methods=['GET', 'POST'])
def results():
   if request.method == 'POST':
      print('postmethod')
      if request.form['csv'] == 'Download Csv':
          print('downloading')
          path = join('.temp', 'final.csv')
          return send_file(
            path,
            as_attachment=True
      ) 
      elif request.form['csv'] == 'Download Image':
          print('downloading')
          path = join('.temp', 'crop.png')
          return send_file(
            path,
            as_attachment=True
      )
   elif request.method == 'GET':
      return render_template('table.html')


@app.route('/', methods=['GET', 'POST'])
def upload():
   if request.method == 'POST':
       if request.files:
           file = request.files["file"]
           path = join(TEMP_DIR, 'input.png')
           file.save(path)
           crop_table(path)
           return redirect(url_for('results'))
   return render_template('index.html')

# @app.route('/at_work')
# def work_page():  
#    return render_template('output.html')

if __name__=='__main__':
   app.run(debug=True, port=4030)