from flask import Flask ,render_template , flash , redirect , url_for, session, request, logging
import pymysql

app = Flask(__name__)
app.debug=True


# db = pymysql.connect(host='localhost', 
#                         port=8000, 
#                         user='root', 
#                         passwd='1234', 
#                         db='myflaskapp')


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register')
def register():
    id = request.form.get(id)
    pw = request.form.get(pw)
    return render_template('register.html')



if __name__ == '__main__':
    # app.secret_key = '1234'
    app.run(host='0.0.0.0', port='8000')