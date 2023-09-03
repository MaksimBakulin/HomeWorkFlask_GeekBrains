from flask import Flask, render_template, request, make_response, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/welcome')
def welcome():
    name = request.cookies.get('name')
    return render_template('welcome.html', name=name)

@app.route('/setcookie', methods=['POST'])
def setcookie():
    name = request.form['name']
    email = request.form['email']
    resp = make_response(redirect('/welcome'))
    resp.set_cookie('name', name)
    resp.set_cookie('email', email)
    return resp

@app.route('/logout')
def logout():
    resp = make_response(redirect('/'))
    resp.delete_cookie('name')
    resp.delete_cookie('email')
    return resp

if __name__ == '__main__':
    app.run(debug=True)