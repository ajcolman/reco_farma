from flask_wtf import FlaskForm
from wtforms import HiddenField, IntegerField, SelectField
from wtforms.validators import DataRequired, NumberRange
class F_Doctores(FlaskForm):
    
    txtPersonaCod = HiddenField("Persona", validators=[DataRequired("El campo de Persona es requerido")])
    txtDoctorMatricula = IntegerField("Matrícula Profesional", validators=[DataRequired(
        "El campo de Matrícula Profesional es requerido"), NumberRange(min=0)])
    sltEspecialidadMedica = SelectField("Especialidad Médica", validators=[DataRequired(
        "El campo de Especialidad Médica es requerido")], coerce=int, default='2')
    sltInstitucionMedica = SelectField("Institución Médica", validators=[DataRequired("El campo de Institución Médica es requerido")], coerce=int, default="1")
    sltEstado = SelectField("Estado", choices=[('A', 'ACTIVO'), ('I', 'INACTIVO')])

