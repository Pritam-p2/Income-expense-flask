from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager

app = Flask(__name__) 
app.config[ 'SQLALCHEMY_DATABASE_URI'] = 'sqlite:///financeDB.db'
app.config[ 'SECRET_KEY']="c@56bf875649b101f93f1195" 
db = SQLAlchemy(app) 
app.app_context().push() 

bcrypt = Bcrypt(app) 
login_manager=LoginManager(app)
login_manager.login_view = "login" # this needed when added login required in routes 
login_manager.login_message_category = "info" 


from app import routes,models
