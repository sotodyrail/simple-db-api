# coding: utf-8
from safrs import SAFRSBase
from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, CheckConstraint, Column, Date, ForeignKey, Integer, SmallInteger, String, Time, text
from flask import current_app as app
import pika
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event

db = SQLAlchemy(app)
db.init_app(app)


class Drug(SAFRSBase, db.Model):
    __tablename__ = 'drug'
    __table_args__ = {'schema': 'medication'}

    id = Column(Integer, primary_key=True)
    drug_name = Column(String(255))


class DutyList(SAFRSBase, db.Model):
    __tablename__ = 'duty_list'
    __table_args__ = {'schema': 'medication'}

    id = Column(SmallInteger, primary_key=True)
    nurse_name = Column(String(100))
    start_shift = Column(Time)


class Patient(SAFRSBase, db.Model):
    __tablename__ = 'patient'
    __table_args__ = {'schema': 'medication'}

    id = Column(Integer, primary_key=True)
    p_name = Column(String(35))
    p_patronymic = Column(String(35))
    p_surname = Column(String(35))
    birth_date = Column(Date)
    medical_policy = Column(String(17))
    contact_phone = Column(String(12))
    type_hospitalization = Column(String(25))
    date_hospitalization = Column(Date)
    discharged = Column(Boolean)


class TreatmentDepartment(SAFRSBase, db.Model):
    __tablename__ = 'treatment_department'
    __table_args__ = {'schema': 'medication'}

    id = Column(Integer, primary_key=True)
    storey = Column(Boolean)
    branch_name = Column(String(35))
    department_head = Column(String(100))
    head_nurse = Column(String(100))
    station_phone = Column(String(11))


class AttendingPhysician(SAFRSBase, db.Model):
    __tablename__ = 'attending_physician'
    __table_args__ = {'schema': 'medication'}

    id = Column(Integer, primary_key=True)
    d_name = Column(String(35))
    d_patronymic = Column(String(35))
    d_surname = Column(String(35))
    start_medical_examination = Column(Time)
    end_medical_examination = Column(Time)
    patient_id = Column(ForeignKey('medication.patient.id'), nullable=False)

    patient = relationship('Patient')


class DeliveryPill(SAFRSBase, db.Model):
    __tablename__ = 'delivery_pills'
    __table_args__ = {'schema': 'medication'}

    id = Column(Integer, primary_key=True)
    nurse_id = Column(ForeignKey('medication.duty_list.id'))
    patient_id = Column(ForeignKey('medication.patient.id'))
    delivered = Column(Boolean)
    time_delivery = Column(Date)

    nurse = relationship('DutyList')
    patient = relationship('Patient')


class Diagnosis(SAFRSBase, db.Model):
    __tablename__ = 'diagnosis'
    __table_args__ = {'schema': 'medication'}

    id = Column(Integer, primary_key=True)
    provisional_diagnosis = Column(String(255))
    refined_diagnosis = Column(String(255))
    date_of_diagnosis = Column(Date)
    dynamics = Column(String(255))
    patient_id = Column(ForeignKey('medication.patient.id', ondelete='CASCADE'), nullable=False, unique=True)

    patient = relationship('Patient', uselist=False)


class Mark(SAFRSBase, db.Model):
    __tablename__ = 'mark'
    __table_args__ = (
        {'schema': 'medication'}
    )

    id = Column(Integer, primary_key=True)
    identifier = Column(Integer, nullable=False, unique=True)
    switch = Column(Boolean, server_default=text("false"))
    patient_id = Column(ForeignKey('medication.patient.id'), nullable=False, unique=True)
    patient = relationship('Patient', uselist=False)


class PrescribedMedication(SAFRSBase, db.Model):
    __tablename__ = 'prescribed_medication'
    __table_args__ = {'schema': 'medication'}

    id = Column(Integer, primary_key=True)
    patient_id = Column(ForeignKey('medication.patient.id', ondelete='CASCADE'), nullable=False)
    drug_id = Column(ForeignKey('medication.drug.id'))

    drug = relationship('Drug')
    patient = relationship('Patient')


class Ward(SAFRSBase, db.Model):
    __tablename__ = 'ward'
    __table_args__ = (
        CheckConstraint('ward_capacity > 0'),
        {'schema': 'medication'}
    )

    id = Column(Integer, primary_key=True)
    ward_capacity = Column(SmallInteger)
    branch_id = Column(ForeignKey('medication.treatment_department.id', ondelete='SET NULL'), nullable=False)

    branch = relationship('TreatmentDepartment')


class Attached(SAFRSBase, db.Model):
    __tablename__ = 'attached'
    __table_args__ = (
        CheckConstraint('place > 0'),
        {'schema': 'medication'}
    )

    id = Column(Integer, primary_key=True)
    patient_id = Column(ForeignKey('medication.patient.id', ondelete='CASCADE'), nullable=False, unique=True)
    ward_id = Column(ForeignKey('medication.ward.id'), nullable=False)
    place = Column(SmallInteger)

    patient = relationship('Patient', uselist=False)
    ward = relationship('Ward')


@event.listens_for(Mark, "before_insert", propagate=True)
@event.listens_for(Mark, "before_update", propagate=True)
def mark_commit(*args, **kwargs):
    print("SIGNAL SEND TO http://localhost:15672/#/queues")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='logs', exchange_type='fanout')
    result = channel.queue_declare(queue='MARK SIGNALS')
    queue_name = result.method.queue
    channel.queue_bind(exchange='logs', queue=queue_name)
    prop = pika.BasicProperties(
        content_type='application/json',
        content_encoding='utf-8',
        headers={'key': 'value'},
        delivery_mode=1,
    )
    model = {c.name: getattr(args[2], c.name) for c in args[2].__table__.columns}
    channel.basic_publish(
        exchange='logs',
        routing_key='MARK SIGNALS',
        properties=prop,
        body=json.dumps(model)
    )
    connection.close()