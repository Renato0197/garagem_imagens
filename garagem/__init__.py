from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

db_url = os.getenv('DATABASE_URL')

# Adicionar porta e sslmode, se estiverem ausentes
if db_url:
    if not '5432' in db_url:
        db_url = db_url.replace(".render.com/", ".render.com:5432/")
    if 'sslmode' not in db_url:
        db_url += '?sslmode=require'

app.config['SQLALCHEMY_DATABASE_URI'] = db_url

app = Flask(__name__)
app.config['SECRET_KEY'] = '01c68762752ec23cd8e9c840595a096a'
app.config['UPLOAD_FODER']= 'static/fotos_post'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'home'
#: view refere-se ao arquivo onde o valor home esta armazenado

from garagem import routes