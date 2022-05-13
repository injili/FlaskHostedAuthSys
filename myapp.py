from flask import Flask,request,render_template,redirect,url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,UserMixin,login_user,login_required,logout_user


import hashlib
import os
import sqlite3
import flask

currentlocation = os.path.dirname(os.path.abspath(__file__))

myapp=Flask(__name__)
myapp.config['SECRET_KEY']='secret'
myapp.config['SQLALCHEMY_DATABASE_URI']='sqlite:////Users/ADMIN/Downloads/git/FlaskAuthSys/database.db'
Bootstrap(myapp)
db = SQLAlchemy(myapp)
login_manager = LoginManager()
login_manager.init_app(myapp)
login_manager.login_view = 'login'
SQLALCHEMY_TRACK_MODIFICATIONS = False

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
@login_manager.user_loader
def load_user(users_id):
    return Users.query.get(int(users_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    
class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid Email'), Length(max=50)])    

class Users(db.Model, UserMixin):
        #code

    def is_active(self):
       return True


    def __repr__(self):
       return " "

@myapp.route('/')
def index():
    return render_template("index.html")

@myapp.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
       users = Users.query.filter_by(username=form.username.data).first()
       if users:
           if users.password == form.password.data:
               login_user(users)
               return redirect(url_for('dashboard'))
       return '<h1> Invalid username or password</h1>'
    return render_template('login.html', form = form)

@myapp.route('/signup', methods=['GET','POST'])
def signup():
    form = RegisterForm()   
    if form.validate_on_submit():
        new_users = Users(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(new_users)
        db.session.commit()
        
        return '<h1>New user has been created!</h1>'
    return render_template('signup.html', form = form)

@myapp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@myapp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
if __name__ == '__main__':
    myapp.run(debug=True)