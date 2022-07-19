from flask import Flask, make_response, redirect, request, render_template, abort, session, request, jsonify, url_for, flash
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, DateField, EmailField
from wtforms.validators import DataRequired, Email
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap


app = Flask(__name__)

app.config['SECRET_KEY'] = 'LLAVE_SECRETA'


class LoginFormSignIn(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar sesión')


class LoginFormSignUp(FlaskForm):
    email = EmailField('Correo', validators=[Email()])
    usernameR = StringField('Usuario', validators=[DataRequired()])
    date = DateField('Nacimiento', validators=[DataRequired()])
    passwordR = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Registrarse')


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database/studily.db"
db = SQLAlchemy(app)


bootstrap = Bootstrap(app)

todos = ['y', 'Horarios', 'Trabajos']


@app.route("/")
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('/home'))
    session['user_ip'] = user_ip
    return response


@app.route('/home', methods=['GET', 'POST'])
def home():
    user_ip = session.get('user_ip')

    login_form = LoginFormSignIn()

    username = session.get('username')
    password = session.get('password')

    session['username'] = username
    session['password'] = password

    print(login_form.username.data, "VIDA HPTAAAAAAAA")
    context = {
        'user_ip': user_ip,
        'todos': todos,
        'login_form': login_form,
        'username': login_form.username.data,
        'password': login_form.password.data
    }

    return render_template('home.html', **context)


@app.route("/login", methods=['GET', 'POST'])
def login():
    user_ip = session.get('user_ip')
    login_form = LoginFormSignIn()
    username = session.get('username')
    password = session.get('password')

    context = {
        'user_ip': user_ip,
        'todos': todos,
        'login_form': login_form,
        'username': username,
        'password': password
    }

    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        session['username'] = username
        session['password'] = password
        flash('Login successful', 'success')
        return redirect(url_for('index'))

    return render_template('login.html', **context)


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    user_ip = session.get('user_ip')
    signup_form = LoginFormSignUp()
    email = session.get('email')
    usernameR = session.get('usernameR')
    date = session.get('date')
    passwordR = session.get('passwordR')

    context = {
        'user_ip': user_ip,
        'todos': todos,
        'signup_form': signup_form,
        'email': email,
        'usernameR': usernameR,
        'date': date,
        'passwordR': passwordR
    }

    if signup_form.validate_on_submit():
        email = signup_form.email.data
        usernameR = signup_form.usernameR.data
        date = signup_form.date.data
        passwordR = signup_form.passwordR.data
        session['email'] = email
        session['usernameR'] = usernameR
        session['date'] = date
        session['passwordR'] = passwordR
        flash('Signup successful', 'success')
        return redirect(url_for('login'))

    return render_template('registro.html', **context)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)


@app.errorhandler(500)
def internal_server_error(error):
    # abort(500)
    return render_template('500.html', error=error)


if __name__ == '__app__':
    app.run()
