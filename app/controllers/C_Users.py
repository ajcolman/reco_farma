from datetime import date
from flask import Blueprint, json, render_template, request
from flask_login import login_required
from app.forms.F_People import F_Busqueda_Persona
from app.forms.F_Users import F_Registro_Usuario
from app.models.Models import People, Roles, Users, db


class C_Users():
    usuarios = Blueprint('usuarios', __name__)

    @usuarios.route('/users')
    @login_required
    def users():
        formBusq = F_Busqueda_Persona()
        formUser = F_Registro_Usuario()
        roles = Roles.query.order_by(Roles.role_desc).all()
        choices = [(rol.role_id, rol.role_desc) for rol in roles]
        formUser.sltRol.choices = choices
        return render_template('v_users.html', title="Listado de Usuarios", formBusq=formBusq, formUser=formUser, roles=roles)

    @usuarios.route('/register_user_data', methods=['POST'])
    @login_required
    def register_user_data():
        message = {"correcto": '', "alerta": '', "error": ''}
        form = F_Registro_Usuario(request.form)
        roles = Roles.query.order_by(Roles.role_desc).all()
        choices = [(rol.role_id, rol.role_desc) for rol in roles]
        form.sltRol.choices = choices
        if form.validate_on_submit():
            persona = form.txtPersonaCod.data
            contrasena = form.txtPassword.data
            rol = form.sltRol.data
            estado = form.sltEstado.data
            user = Users.query.filter_by(user_peop_id=form.txtPersonaCod.data).first()
            person_data = People.query.filter_by(peop_id = persona).first()
            if user is not None:
                # Actualizar los datos del usuario
                if contrasena!="":
                    user.user_password = Users.hash_password(contrasena)
                user.user_name = person_data.peop_dni
                user.user_role_id = rol
                user.user_updated_id = 1
                user.user_state = estado
                db.session.commit()
            else:
                # Registrar el usuario nuevo
                user = Users()
                user.user_peop_id = persona
                user.user_name = person_data.peop_dni
                if contrasena!="":
                    user.user_password = Users.hash_password(contrasena)
                user.user_role_id = rol
                user.user_created_id = 1
                user.user_state = estado
                db.session.add(user)
                db.session.commit()
            message['correcto'] = '<strong>Se ha realizado correctamente el registro de los datos del usuario</strong>'
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
    
    @usuarios.route('/get_users_list', methods=['GET'])
    @login_required
    def get_users_list():
        message = {"correcto": '', "alerta": '', "error": ''}
        users = Users.query.with_entities(Users.user_id.label("id"), Users.user_name.label("username"), (People.peop_names + ' ' + People.peop_lastnames).label("person"), Users.user_peop_id.label("peop_id"), Users.user_state.label("state"), Roles.role_id.label("role_id"), Roles.role_desc.label("role")).join(People, People.peop_id == Users.user_peop_id, isouter=True).join(Roles, Roles.role_id == Users.user_role_id).paginate(
            page=request.args.get('page', 1), per_page=10)
        return {
            'data': 
            [
                {
                    "id": user.id,
                    "username": user.username,
                    "person": user.person,
                    "person_id": user.peop_id,
                    "state": user.state,
                    "state_full": "ACTIVO" if user.state == "A" else "INACTIVO",
                    "role_desc": user.role,
                    "role_id": user.role_id,
                } for user in users
            ] ,
            'total': users.total
        }
