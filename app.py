from flask import Flask ,render_template , flash , redirect , url_for, session, request, logging, make_response
import pymysql
from passlib.hash import pbkdf2_sha256 as pbk
from functools import wraps

import logging
import eventlet
from time import time
import json
from flask_bootstrap import Bootstrap
import paho.mqtt.client as paho
from datetime import datetime
import random
from random import random


app = Flask(__name__)
app.debug=True

db = pymysql.connect(host='localhost', 
                        port=3306, 
                        user='root', 
                        passwd='1234', 
                        db='team2')

name = ['']
live_data = [0]



def is_logged_in(f):
    @wraps(f)
    def wrap (*args, **kwargs):
        if 'is_logged' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap

def is_logged_out(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'is_logged' in session:
            return redirect(url_for('login'))
        else:
            return f(*args, **kwargs)
    return wrap


@app.route('/')
@is_logged_in
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':

        name = request.form['name']
        username = request.form.get('username')
        email = request.form.get('email')
        password = pbk.hash(request.form.get('password'))
        re_password = request.form.get('re_password')

        # print(name, email)

        cursor = db.cursor()
        sql = '''
                    INSERT INTO users (name , email , username , password) 
                    VALUES (%s ,%s, %s, %s )
              '''
        cursor.execute(sql, (name, email, username, password))
        db.commit()
        
    
        return redirect(url_for('login'))

    else:
        # print("실행안됨")
        return render_template('register.html')
        db.close()

@app.route('/login', methods=['GET','POST'])
@is_logged_out
def login():
    if request.method == 'POST':
        un = request.form['username']
        pw = request.form.get('password')
        sql = 'SELECT * FROM users WHERE username = %s'
        cursor = db.cursor()
        cursor.execute(sql, [un])
        users = cursor.fetchone()

        if users==None:
            print("유저가 없다")
            return render_template('login.html')
        else:
            if pbk.verify(pw, users[4]):
                session['username'] = users[3]
                session['is_logged'] = True
                name[0] = session['username']
                print(name[0])
                print(session['username'])
                return redirect(url_for('home'))
            else:
                print("정보가 다릅니다")
                return render_template('login.html')

        return 'Success'
    else:
        print('실행안됨')
        return render_template("login.html")
   
    return render_template("login.html")
    db.close()

@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    # print(session['is_logged'], session['username'])
    return redirect(url_for('home'))

def on_connect( client, userdata, flags, rc):
    print ("connect with result code "+str(rc))
    client.subscribe("temp")



def on_message(client, userdata, message):
    recvData = str(message.payload.decode("utf-8"))
    # jsonData = json.loads(recvData) #json 데이터를 dict형으로 파싱      
    # sql_select = 'SELECT username FROM users WHERE '
    sql_insert =    '''
                        INSERT INTO data (username, temp) 
                        VALUES(%s, %s)
                    '''
    cursor = db.cursor()
    # cursor.execute(sql_select)
    # username = cursor.fetchone
    print(name[0])
    cursor.execute(sql_insert, [name, recvData])
    db.commit()


    # print("recvData : "+recvData)
     


client = paho.Client()
client.connect('localhost', 1883, 60)
client.on_connect = on_connect
client.on_message = on_message

# client.loop_stop()

@app.route('/data')
@is_logged_in
def data():
    
    client.loop_start()
    client.loop_stop()   
    
    cursor = db.cursor()

    sql_select =    '''
                        SELECT temp From data 
                    '''
    cursor.execute(sql_select)
    temp = cursor.fetchall()
    live_data[0] = temp[-1][0]
    # print(live_data)
    return temp[-1][0]
    # 데이터를 불러옴
 
@app.route('/database')
@is_logged_in
def database():
    return render_template("database.html")


# @app.route('/livechart', methods=["GET", "POST"])
# def main():
#     return render_template('livechart.html')


@app.route('/livechart')
def livechart():
    chdata = [time() * 1000, float(live_data[0])]
    # chdata = [time() * 1000, random() * 100]
    print(chdata)
    response = make_response(json.dumps(chdata))
    response.content_type = 'application/json'
    return response

# @app.route('/graph')
# def graph():
#     list_data = [0, 10, 5, 2, 20, 30, 45, 100, 40]
#     return render_template('graph.html', list_data = list_data)


if __name__ == '__main__':
    app.secret_key = '1234'
    app.run(host='0.0.0.0', port='8000')
    # socketio.run(app, host='0.0.0.0', port=8000, use_reloader=False, debug=True)