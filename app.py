from flask import Flask ,render_template , flash , redirect , url_for, session, request, logging
import pymysql

app = Flask(__name__)
app.debug=True


db = pymysql.connect(host='localhost', 
                        port=3306, 
                        user='root', 
                        passwd='1234', 
                        db='team2')


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':

        name = request.form['name']
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        re_password = request.form.get('re_password')

        print(name, email)

        cursor = db.cursor()
        sql = '''
                    INSERT INTO users (name , email , username , password) 
                    VALUES (%s ,%s, %s, %s )
              '''
        cursor.execute(sql, (name, email, username, password))
        db.commit()
        
        return redirect(url_for('login'))
    
    else:
        print("실행안됨")
        return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/graph')
def graph():
    list_data = [0, 10, 5, 2, 20, 30, 45, 100, 40]
    return render_template('graph.html', list_data = list_data)

if __name__ == '__main__':
    app.secret_key = '1234'
    app.run(host='0.0.0.0', port='8000')