from flask import Blueprint, render_template


class C_Doctors():
    doctors = Blueprint('doctors', __name__)

    @doctors.route('/doctors_register')
    def doctors_register():
        render_template('v_doctor_register.html', title="Registro de Médico")