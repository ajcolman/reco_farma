from flask import Blueprint, json, redirect, render_template, session, url_for
from flask_login import current_user, login_user

from app.forms.F_Login import F_Login
from app.models.Models import People, Users
class C_Login():
    login = Blueprint('login',__name__)
    @login.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('login.principal'))
        form = F_Login()
        return render_template('v_login.html', title='Login', form=form)
    
    @login.route('/process_user_credentials', methods=['POST'])
    def process_user_credentials():
        message = {"correcto": '', "alerta": '', "error": ''}
        form = F_Login()
        if form.validate_on_submit():
            usuario = form.txtUsuario.data
            contrasena = form.txtPassword.data
            user_data = Users.query.filter_by(user_name = usuario, user_state = 'A').first()
            if user_data is not None:
                password_hash = user_data.user_password
                if Users.check_password_hash(password_hash,contrasena):
                    login_user(user_data)
                    person_people = People.query.filter_by(peop_id = user_data.user_peop_id).first()
                    session['logged'] = True
                    session['user_id'] = user_data.user_id
                    session['habilitation'] = user_data.user_state
                    session['person'] = person_people.peop_names + ' ' + person_people.peop_lastnames
                    message['correcto'] = "Se ha comprobado las credenciales"
                else:
                    message['error'] = "Usuario o contraseña incorrectas"
            else:
                message['error'] = "El usuario ingresado no existe o ha sido bloqueado"
        else:
            errores = {}
            for campo, errores_campo in form.errors.items():
                label = form[campo].label.text
                errores[campo] = '{}: {} <br>'.format(
                    label, ', '.join(errores_campo))
            message['error'] = {}
            message['error']['validacion'] = '<strong>Por favor, corrija los errores en el formulario.</strong><br>'
            message['error']['detalles'] = errores
        return json.dumps(message)
    
    @login.route('/principal')
    def principal():
        return render_template('v_principal.html', title="Bienvenido")
