from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
db = SQLAlchemy()

class Roles(db.Model):
    __tablename__ = 'roles'
    role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_desc = db.Column(db.String(100), unique=True, nullable=False)


class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(10), unique=True, nullable=False)
    user_password = db.Column(db.String(255), nullable=False)
    user_state = db.Column(db.String(1), default='A')
    user_role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'), nullable=False)
    user_created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_created_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    user_updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    user_updated_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    user_peop_id = db.Column(db.Integer, db.ForeignKey('people.peop_id'))
    user_register = db.relationship(
        'Users', backref='users_register', foreign_keys=[user_created_id], remote_side=[user_id])
    user_modifier = db.relationship(
        'Users', backref='users_modifier', foreign_keys=[user_updated_id], remote_side=[user_id])
    
    def hash_password(password):
        return generate_password_hash(password)
    def check_password_hash(password_hash,contrasena):
        return check_password_hash(password_hash, contrasena)
    def is_active(self):
        return self.user_state
    
    def get_id(self):
        return self.user_id

class People(db.Model):
    __tablename__ = 'people'
    peop_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    peop_names = db.Column(db.String(100), nullable=False)
    peop_lastnames = db.Column(db.String(100), nullable=False)
    peop_dni = db.Column(db.String(8), unique=True, nullable=False)
    peop_gender = db.Column(db.String(1), nullable=False)
    peop_birthdate = db.Column(db.Date(), nullable=False)
    peop_created_at = db.Column(db.DateTime, default=datetime.utcnow)
    peop_user_created_id = db.Column(
        db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    peop_updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    peop_user_updated_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    peop_register = db.relationship(
        'Users', backref='peop_register', foreign_keys=[peop_user_created_id])
    peop_modifier = db.relationship(
        'Users', backref='peop_modifier', foreign_keys=[peop_user_updated_id])

class Doctors(db.Model):
    __tablename__ = "doctors"
    doct_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    doct_peop_id = db.Column(db.Integer, db.ForeignKey('people.peop_id'), nullable=False)
    doct_professional_registration = db.Column(db.String(20), nullable=False)
    doct_state = db.Column(db.String(1), default='A', nullable=False)
    doct_created_at = db.Column(db.DateTime, default=datetime.utcnow)
    doct_user_created_id = db.Column(
        db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    doct_updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    doct_user_updated_id = db.Column(
        db.Integer, db.ForeignKey('users.user_id'))
    doct_register = db.relationship(
        'Users', backref='doct_register', foreign_keys=[doct_user_created_id])
    doct_modifier = db.relationship(
        'Users', backref='doct_modifier', foreign_keys=[doct_user_updated_id])

class PeoplePrescription(db.Model):
    __tablename__ = "people_prescription"
    pepr_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pepr_peop_id = db.Column(db.Integer, db.ForeignKey('people.peop_id'), nullable=False)
    pepr_doct_id = db.Column(db.Integer, db.ForeignKey('doctors.doct_id'), nullable=False)
    pepr_state = db.Column(db.String(1), default='A', nullable=False)
    pepr_created_at = db.Column(db.DateTime, default=datetime.utcnow)
    pepr_user_created_id = db.Column(
        db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    pepr_updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    pepr_user_updated_id = db.Column(
        db.Integer, db.ForeignKey('users.user_id'))
    pepr_register = db.relationship(
        'Users', backref='pepr_register', foreign_keys=[pepr_user_created_id])
    pepr_modifier = db.relationship(
        'Users', backref='pepr_modifier', foreign_keys=[pepr_user_updated_id])

class PeoplePrescriptionDetails(db.Model):
    __tablename__ = "people_prescription_details"
    prde_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prde_pepr_id = db.Column(db.Integer, db.ForeignKey('people_prescription.pepr_id'), nullable=False)
    prde_details = db.Column(db.String(4000), nullable=False)
    prde_state = db.Column(db.String(1), default='A', nullable=False)
    prde_created_at = db.Column(db.DateTime, default=datetime.utcnow)
    prde_user_created_id = db.Column(
        db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    prde_updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    prde_user_updated_id = db.Column(
        db.Integer, db.ForeignKey('users.user_id'))
    prde_register = db.relationship(
        'Users', backref='prde_register', foreign_keys=[prde_user_created_id])
    prde_modifier = db.relationship(
        'Users', backref='prde_modifier', foreign_keys=[prde_user_updated_id])
    
class PeoplePhotos(db.Model):
    __tablename__ = 'people_photos'
    peph_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    peph_path = db.Column(db.String(100), nullable=False)
    peph_peop_id = db.Column(db.Integer, db.ForeignKey('people.peop_id'), nullable=False)
    peph_state = db.Column(db.String(1), default='A', nullable=False)
    peph_created_at = db.Column(db.DateTime, default=datetime.utcnow)
    peph_user_created_id = db.Column(
        db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    peph_updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    peph_user_updated_id = db.Column(
        db.Integer, db.ForeignKey('users.user_id'))
    peph_register = db.relationship(
        'Users', backref='peph_register', foreign_keys=[peph_user_created_id])
    peph_modifier = db.relationship(
        'Users', backref='peph_modifier', foreign_keys=[peph_user_updated_id])
