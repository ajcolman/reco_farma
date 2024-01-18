from flask import Blueprint, render_template


class C_Pharma():
    pharma = Blueprint('pharma', __name__)
    
    @pharma.route('/medical_prescriptions')
    def medical_prescriptions():
        return render_template('v_medical_prescriptions.html', title="Ver Prescripciones Médicas")