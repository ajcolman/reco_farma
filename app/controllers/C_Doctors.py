from flask import Blueprint, render_template
from app.forms.F_Doctors import F_Doctores
from app.forms.F_People import F_Busqueda_Persona
from app.models.Models import Institutions, MedicalEspecialties


class C_Doctors():
    doctors = Blueprint('doctors', __name__)

    @doctors.route('/doctors_register')
    def doctors_register():
        formBusq = F_Busqueda_Persona()
        formDoct = F_Doctores()
        me = [(ep.mees_id, ep.mees_desc) for ep in MedicalEspecialties.query.all()]
        formDoct.sltEspecialidadMedica.choices=me
        inst = [(i.inst_id, i.inst_trade_name) for i in Institutions.query.all()]
        formDoct.sltInstitucionMedica.choices = inst
        return render_template('v_doctors_register.html', title="Registro de Médicos", formBusq=formBusq, formDoct=formDoct)
