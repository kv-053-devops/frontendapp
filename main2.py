from flask import Flask, render_template, request
app = Flask(__name__)
#...
@app.route('/login/', methods=['post', 'get'])
def login():
    message = ''
    if request.method == 'POST':
        username = request.form.get('username')  # запрос к данным формы
        password = request.form.get('password')
        if username == 'root' and password == 'pass':
            message = "Correct username and password"
        else:
            message = "Wrong username or password"
    return render_template('login.html', message=message)
#...

@app.route('/')
def hello_world():
    return 'Task for flask'

if __name__ == '__main__':
    app.run()
