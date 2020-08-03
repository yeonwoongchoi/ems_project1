from flask import Flask ,render_template , flash , redirect , url_for, session, request, logging
import pymysql
from passlib.hash import pbkdf2_sha256 as pbk
from functools import wraps

import logging
import eventlet
import json
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap

eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET'] = 'my secret key'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = 'localhost'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_CLIENT_ID'] = 'flask_mqtt'
app.config['MQTT_CLEAN_SESSION'] = True
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False
app.config['MQTT_LAST_WILL_TOPIC'] = 'home/lastwill'
app.config['MQTT_LAST_WILL_MESSAGE'] = 'bye'
app.config['MQTT_LAST_WILL_QOS'] = 2
app.debug=True


# Parameters for SSL enabled
# app.config['MQTT_BROKER_PORT'] = 8883
# app.config['MQTT_TLS_ENABLED'] = True
# app.config['MQTT_TLS_INSECURE'] = True
# app.config['MQTT_TLS_CA_CERTS'] = 'ca.crt'


db = pymysql.connect(host='localhost', 
                        port=3306, 
                        user='root', 
                        passwd='1234', 
                        db='team2')



mqtt = Mqtt(app)
socketio = SocketIO(app)
bootstrap = Bootstrap(app)


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



@socketio.on('publish')
def handle_publish(json_str):
    data = json.loads(json_str)
    mqtt.publish(data['topic'], data['message'], data['qos'])


@socketio.on('subscribe')
def handle_subscribe(json_str):
    data = json.loads(json_str)
    mqtt.subscribe(data['topic'], data['qos'])


@socketio.on('unsubscribe_all')
def handle_unsubscribe_all():
    mqtt.unsubscribe_all()


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode(),
        qos=message.qos,
    )
    socketio.emit('mqtt_message', data=data)

@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    # print(level, buf)
    pass


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

@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    # print(session['is_logged'], session['username'])
    return redirect(url_for('home'))


@app.route('/database')
def database():
    return render_template('database.html')


# @app.route('/graph')
# def graph():
#     list_data = [0, 10, 5, 2, 20, 30, 45, 100, 40]
#     return render_template('graph.html', list_data = list_data)


if __name__ == '__main__':
    app.secret_key = '1234'
    # app.run(host='0.0.0.0', port='8000')
    socketio.run(app, host='0.0.0.0', port=8000, use_reloader=False, debug=True)