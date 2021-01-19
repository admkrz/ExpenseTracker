import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

#Configure app
app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(32)

#Configuring sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

#Encrypting for passwords
bcrypt = Bcrypt(app)

#Initializing user session handler
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from expensetracker import routes

#Initialize database
# db.drop_all()
db.create_all()
db.session.commit()
