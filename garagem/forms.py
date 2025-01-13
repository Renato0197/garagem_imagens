from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField, FileField
from wtforms.validators import DataRequired, Email, Length,EqualTo,ValidationError
from garagem.models import Usuario

class Form_login(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()] )
    senha = PasswordField('Senha', validators=[DataRequired()])
    lembrardados = BooleanField('Lembrar dados')
    botao_entrar = SubmitField('Confirmar')
    def validate_email(self, email):
        usuario= Usuario.query.filter_by(email=email.data).first()
        if not usuario:
            raise ValidationError('não existe uma conta com este email')


class Form_cadastro(FlaskForm):
    username = StringField('Nome de Usuario', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired(),  Length(6,20)])
    confirmasenha = PasswordField('Confirma senha', validators=[DataRequired(), EqualTo('senha')])
    submit_criarconta = SubmitField('Criar Conta')

    def validate_email(self, email):
        usuario= Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Já existe uma conta com este email')

class Form_foto(FlaskForm):
    titulo = StringField('Descrição', validators=[DataRequired()])
    foto = FileField('Imagem', validators=[DataRequired()])
    botao_submit_post = SubmitField('enviar')
