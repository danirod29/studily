from ensurepip import bootstrap
from flask import Flask, make_response, redirect, request, render_template, abort
from flask_bootstrap import Bootstrap


app = Flask(__name__)
bootstrap = Bootstrap(app)

todos = ['Studily', 'Horarios', 'Trabajos']


@app.route("/")
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('/hello'))
    response.set_cookie('user_ip', user_ip)
    return response


@app.route('/hello')
def hello():
    user_ip = request.cookies.get('user_ip')
    context = {
        'user_ip': user_ip,
        'todos': todos,
    }
    return render_template('hello.html', **context)
    #'Nada, tu ip es {}'.format(user_ip)


@app.route("/logeado")
def login():
    return render_template('logeado.html')


@app.route("/registrado")
def signup():
    return render_template('registro.html')


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)


@app.errorhandler(500)
def internal_server_error(error):
    # abort(500)
    return render_template('500.html', error=error)
