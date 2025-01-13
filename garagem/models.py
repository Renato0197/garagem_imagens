from garagem import database, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_usuario(id_usuario):
    #é uma função obrigatorial do loginmaneger para reconhecer o id de usuario
    return Usuario.query.get(int(id_usuario))

class Usuario(database.Model, UserMixin):
    #usermixin diz qua é a classe que vai gerenciar a estrutura de login
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False, unique=True)
    foto = database.relationship('Foto', backref='usuario', lazy=True)

class Foto(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False, default=' ')
    imagem = database.Column(database.String, nullable=False, default='padrao.png')
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
