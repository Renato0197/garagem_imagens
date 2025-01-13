from garagem import app, database, bcrypt
from flask import render_template, url_for, request, flash, redirect
from flask_login import login_required, login_user, logout_user, current_user
from garagem.forms import Form_login, Form_cadastro, Form_foto
from garagem.models import Usuario, Foto
import os
from werkzeug.utils import secure_filename
from sqlalchemy import func
from time import sleep

@app.route('/', methods = ['GET','POST'])
def home():
    login = Form_login()
    if login.validate_on_submit():
        usuario= Usuario.query.filter_by(email=login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, login.senha.data):
            login_user(usuario, remember=True)
            return redirect(url_for('perfil', id_usuario=usuario.id))
    return render_template('home.html', form=login)

@app.route('/atualizar-conteudo')
def atualizar_conteudo():
    foto = Foto.query.order_by(func.random()).limit(1).scalar()  # Busca uma foto aleatória
    if foto:
        imagem_url = url_for('static', filename=f'fotos_post/{foto.imagem}')
        return f'''
            <img src="{imagem_url}" alt="Imagem dinâmica" class="quadro" >
        '''
    else:
        return '''
            <img src="{url_for('static', filename='fotos_post/default.jpg')}" alt="Imagem padrão class="quadro" >

        '''

@app.route('/cadastro', methods = ['GET','POST'])
def cadastro():
    cadastro= Form_cadastro()
    if cadastro.validate_on_submit():
        #este if verifica se o botão de confirmação foi apertado e se o dados estão preenchidos corretamente
        senha_criptografada= bcrypt.generate_password_hash(cadastro.senha.data)
        usuario= Usuario(username= cadastro.username.data, email = cadastro.email.data ,senha= senha_criptografada)
        #a variavel acima recebe como valor os dados dos campos do formulario
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        #o trecho acima fará com que ousuario permaneça logao apos cria a contar
        return redirect(url_for('perfil', id_usuario=usuario.id))
        #acima, a variavel usuario serar usada para dar o valor da vriavel usuario da pagina perfil
    return render_template('cadastro.html', form=cadastro)

@app.route('/perfil/<id_usuario>', methods=['GET','POST'])
@login_required
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id):
        form_foto = Form_foto()
        if form_foto.validate_on_submit():
            titulo = form_foto.titulo.data
            arquivo = form_foto.foto.data
            nomeseguro = secure_filename(arquivo.filename)
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FODER'], nomeseguro)
            arquivo.save(caminho)
            foto = Foto(imagem=nomeseguro, titulo=titulo, id_usuario=current_user.id)
            database.session.add(foto)
            database.session.commit()
            return redirect(url_for('perfil', id_usuario=current_user.id))
        return render_template('perfil.html', usuario=current_user, form=form_foto)
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template('perfil.html', usuario=usuario, form=None)

@app.route('/sair')
@login_required
def sair():
    logout_user()
    return redirect(url_for('home'))

@app.route('/feed')
@login_required
def feed():
    fotos= Foto.query.order_by(Foto.data_criacao.desc()).all()
    return render_template('feed.html', fotos=fotos)