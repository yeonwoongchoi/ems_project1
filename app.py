from flask import Flask ,render_template
from data import signin
app = Flask(__name__)
app.debug=True

@app.route('/')
def index():
    print("Success")
    # return "TEST"
    return render_template('home.html')

if __name__ =='__main__':
    app.run(host='0.0.0.0', port='8000')
    app.run()

@app.route('/Sign in')
def about():
    print("Success")
    # return "TEST"
    return render_template('about.html',hello="GaryKim")