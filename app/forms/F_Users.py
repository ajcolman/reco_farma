from flask_wtf import FlaskForm
from wtforms import HiddenField, IntegerField, PasswordField, SelectField, StringField
from wtforms.validators import DataRequired, Length
class F_Registro_Usuario(FlaskForm):
    txtPersonaCod = HiddenField('Persona', validators=[DataRequired()])
    txtPassword = StringField('Contraseña')
    sltRol = SelectField('Apellidos', coerce=int)
    sltEstado = SelectField("Estado", choices=[('A', 'ACTIVO'), ('I', 'INACTIVO')])
