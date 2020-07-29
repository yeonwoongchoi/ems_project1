from flask import Flask ,render_template , flash , redirect , url_for, session, request, logging

import pymysql
from passlib.hash import pbkdf2_sha256
from functools import wraps
app = Flask(__name__)
app.debug=True


db = pymysql.connect(host='localhost', 
                        port=3306, 
                        user='root', 
                        passwd='1234', 
                        db='team2')


#init mysql 
# mysql = MySQL(app)
# cur  = mysql.connection.cursor()
# result  = cur.execute("SELECT * FROM users;")

# users  = cur.fetchall()
# print(users)
# print(result)

def is_LOGED_out(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'is_LOGED' in session:
        # if session['is_LOGED'] :
            return redirect(url_for('/'))
        else:
            return f(*args, **kwargs)

    return wrap


@app.route('/register',methods=['GET' ,'POST'])
@is_LOGED_out
def register():
    if request.method == 'POST':
        # data = request.body.get('author')
        name = request.form.get('name')
        email = request.form.get('email')
        password = pbkdf2_sha256.hash(request.form.get('password'))
        re_password = request.form.get('re_password')
        username = request.form.get('username')
        # name = form.name.data
        cursor = db.cursor()
        sql = 'SELECT username FROM users WHERE username=%s'
        cursor.execute(sql,[username])
        username_1 = cursor.fetchone()
        if username_1 :
            return redirect(url_for('register'))
        else:
            

            if(pbkdf2_sha256.verify(re_password,password )):
                print(pbkdf2_sha256.verify(re_password,password ))
                
                sql = '''
                    INSERT INTO users (name , email , username , password) 
                    VALUES (%s ,%s, %s, %s )
                '''
                cursor.execute(sql , (name,email,username,password ))
                db.commit()
                

                # cursor = db.cursor()
                # cursor.execute('SELECT * FROM users;')
                # users = cursor.fetchall()
                
                return redirect(url_for('login'))

            else:
                return redirect(url_for('register'))

        db.close()
    else:
        return render_template('register.html')


@app.route('/login',methods=['GET', 'POST'])
@is_LOGED_out
def login():
    if request.method == 'POST':
        id = request.form['username']
        pw = request.form.get('password')
        print([id])

        sql='SELECT * FROM users WHERE username = %s'
        cursor = db.cursor()
        cursor.execute(sql, [id])
        users = cursor.fetchone()
        print(users)

        if users ==None:
            return redirect(url_for('login'))
        else:
            if pbkdf2_sha256.verify(pw,users[4] ):
                session['is_LOGED'] = True
                session['username'] = users[3]
                print(session)
                return redirect('/')
            else:
                return redirect('url_for("login")')
        
    else:
        return render_template('login.html')



def is_LOGED_in(f):
    @wraps(f)
    def _wraper(*args, **kwargs):
        if 'is_LOGED' in session:
        # if session['is_LOGED'] :
            return f(*args, **kwargs)

        else:
            flash('UnAuthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return _wraper


@app.route('/logout')
@is_LOGED_in
def logout():
    session.clear()
    return redirect(url_for('login'))
    

@app.route('/')
# @is_LOGED_in

def index():
    print("Success")
    # session['test']= "Gary Kim"
    # session_data = session
    # print(session_data)
    # return "TEST"
    return render_template('home.html')
    

if __name__ =='__main__':
    # app.run(host='0.0.0.0', port='8080')
    
    # Session 실행시 설정
    # 오류: Set the secret_key on the application to something unique and secret.
    app.secret_key = 'secretKey1234'
    # 서버실행
    app.run()