# coding: utf-8
from safrs import SAFRSBase
from sqlalchemy import BigInteger, Boolean, Column, Date, DateTime, ForeignKey, Integer, SmallInteger, String, Table, Time, text
from sqlalchemy.orm import relationship
import sys, inspect

from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy as sqlalchemy

db = sqlalchemy(app)
db.init_app(app)

class AttendingPhysician(SAFRSBase, db.Model):
    __tablename__ = 'attending_physician'
    __table_args__ = {'schema': 'medication'}

    attending_physician_id = Column(Integer, primary_key=True)
    d_name = Column(String(35))
    d_patronymic = Column(String(35))
    d_surname = Column(String(35))
    start_medical_examination = Column(Time)
    end_medical_examination = Column(Time)
    fk_patient_id = Column(ForeignKey('medication.patient.patient_id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, unique=True)

    fk_patient = relationship('Patient')


class DeliveryPill(SAFRSBase, db.Model):
    __tablename__ = 'delivery_pills'
    __table_args__ = {'schema': 'medication'}

    adelivery_pills_id = Column(Integer, primary_key=True)
    ward = Column(Integer)
    delivered = Column(Boolean)
    time_delivery = Column(DateTime(True))
    fk_nurse_id = Column(ForeignKey('medication.duty_list.nurse_id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True)
    fk_patient_id = Column(ForeignKey('medication.patient.patient_id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True)

    fk_nurse = relationship('DutyList')
    fk_patient = relationship('Patient')


class Diagnosis(SAFRSBase, db.Model):
    __tablename__ = 'diagnosis'
    __table_args__ = {'schema': 'medication'}

    diagnosis_id = Column(Integer, primary_key=True)
    provisional_diagnosis = Column(String(255))
    refined_diagnosis = Column(String(255))
    date_of_diagnosis = Column(Date)
    dynamics = Column(String(255))
    fk_patient_id = Column(ForeignKey('medication.patient.patient_id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, unique=True)

    fk_patient = relationship('Patient')


class DutyList(SAFRSBase, db.Model):
    __tablename__ = 'duty_list'
    __table_args__ = {'schema': 'medication'}

    nurse_id = Column(Integer, primary_key=True)
    nurse_name = Column(String(100))
    start_shift = Column(Time)


class Mark(SAFRSBase, db.Model):
    __tablename__ = 'mark'
    __table_args__ = {'schema': 'medication'}

    cell_id = Column(BigInteger, primary_key=True)
    identifier = Column(String(255), nullable=False, unique=True)
    switch = Column(Boolean)
    fk_patient_id = Column(ForeignKey('medication.patient.patient_id', ondelete='RESTRICT', onupdate='RESTRICT'), unique=True)

    fk_patient = relationship('Patient')


class Patient(SAFRSBase, db.Model):
    __tablename__ = 'patient'
    __table_args__ = {'schema': 'medication'}

    patient_id = Column(BigInteger, primary_key=True)
    p_name = Column(String(35))
    p_patronymic = Column(String(35))
    p_surname = Column(String(35))
    birth_date = Column(Date)
    medical_policy = Column(String(16))
    contact_phone = Column(String(11))
    type_hospitalization = Column(String(25))
    date_hospitalization = Column(Date)
    discharged = Column(Boolean)


class PrescribedMedication(SAFRSBase, db.Model):
    __tablename__ = 'prescribed_medication'
    __table_args__ = {'schema': 'medication'}

    enumerator = Column(BigInteger, primary_key=True)
    drug_name = Column(String(255))
    fk_patient_id = Column(ForeignKey('medication.patient.patient_id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True)

    fk_patient = relationship('Patient')


class TreatmentDepartment(SAFRSBase, db.Model):
    __tablename__ = 'treatment_department'
    __table_args__ = {'schema': 'medication'}

    branch_id = Column(Integer, primary_key=True)
    floor = Column(SmallInteger)
    branch_name = Column(String(35))
    department_head = Column(String(100))
    head_nurse = Column(String(100))
    station_phone = Column(String(11))


class User(SAFRSBase, db.Model):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'medication'}

    id = Column(BigInteger, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(BigInteger, nullable=False)


class Ward(SAFRSBase, db.Model):
    __tablename__ = 'ward'
    __table_args__ = {'schema': 'medication'}

    ward_id = Column(Integer, primary_key=True)
    ward = Column(Integer)
    ward_capacity = Column(SmallInteger)
    position = Column(SmallInteger)
    fk_patient_id = Column(ForeignKey('medication.patient.patient_id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, unique=True)
    fk_branch_id = Column(ForeignKey('medication.treatment_department.branch_id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True)

    fk_branch = relationship('TreatmentDepartment')
    fk_patient = relationship('Patient')

