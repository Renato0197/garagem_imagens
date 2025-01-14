from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://db_garagem_user:c4J9iYQexqw3fdT3s3qpWiQVTPD0Jfqo@dpg-cu2ncajqf0us73bprh4g-a.oregon-postgres.render.com/db_garagem"
app.config['SECRET_KEY'] = '01c68762752ec23cd8e9c840595a096a'
app.config['UPLOAD_FODER']= 'static/fotos_post'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'home'
#: view refere-se ao arquivo onde o valor home esta armazenado

from garagem import routes