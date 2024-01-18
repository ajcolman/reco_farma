#Run pip install flask-blueprint
from flask import Blueprint, json, render_template, request

from app.models.Models import Institutions, MedicalEspecialties
class C_Maintenance():
    maint = Blueprint('maint',__name__)
    
    @maint.route('/maintenance')
    def maintenance():
        return render_template('v_maintenance.html', title="Mantenimiento de Datos")
    
    @maint.route('/get_medical_especialties')
    def get_medical_especialties():
        medical_especialties = MedicalEspecialties.query.order_by(MedicalEspecialties.mees_desc).paginate(
            page=request.args.get('page', 1), per_page=10)
        return json.dumps([{
            "id": mees.mees_id,
            "desc": mees.mees_desc,
            "state": mees.mees_state,
            "state_desc": "ACTIVO" if mees.mees_state =="A" else "INACTIVO",
        } for mees in medical_especialties
        ])
        
    @maint.route('/get_medical_institutes')
    def get_medical_institutes():
        medical_institutes = Institutions.query.order_by(Institutions.inst_trade_name).paginate(
            page=request.args.get('page', 1), per_page=10)
        return json.dumps([{
            "id": inst.inst_id,
            "trade_name": inst.inst_trade_name,
            "bussiness_name": inst.inst_bussiness_name,
            "itin": inst.inst_itin,
            "state": inst.inst_state,
            "state_desc": "ACTIVO" if inst.inst_state =="A" else "INACTIVO",
        } for inst in medical_institutes
        ])