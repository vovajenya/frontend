from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import db_handler


# app initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissupposedtobesecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/elahav109995/PycharmProjects/flask_proj/db/database.db'
app.config['SQLALCHEMY_BINDS'] = {'stocks_db':'sqlite:////Users/elahav109995/PycharmProjects/flask_proj/db/stocks_db.db'}
app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_PASSWORD_HASH'] = 'plaintext'
app.debug = True
Bootstrap(app)
db = SQLAlchemy(app)

# stocks DB init
# DB_NAME = 'c:/Users/elahav109995/PycharmProjects/flask_proj/db/stocks_db.db'
# DB = db_handler.DB_Handler()
# DB.create_db(DB_NAME)

# login manager initialization
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# user class
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

# user logging in
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# forms = login and register
class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


# methods
# index
@app.route('/')
def index():
    return render_template('index.html')

# login
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))
        return '<h1>' + 'Invalid username of password' + '</h1>'
    return render_template('login.html', form=form)

# register new user
@app.route('/signup', methods=['GET','POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return '<h1>' + 'new user has been created' + '</h1>'
    return render_template('signup.html', form=form)

# profile page
@app.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    # read table from DB

    DB_NAME = 'c:/Users/elahav109995/PycharmProjects/flask_proj/db/stocks_db.db'
    DB = db_handler.DB_Handler()
    DB.create_db(DB_NAME)
    items = DB.read_all_as_dict()

    return render_template('dashboard.html',name=current_user.username, items=items)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect((url_for('index')))

if __name__ == "__main__":
    app.run()
