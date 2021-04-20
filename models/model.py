# coding: utf-8
from sqlalchemy import BigInteger, Boolean, Column, Date, DateTime, ForeignKey, Integer, SmallInteger, String, Table, Time, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


t_attending_physician = Table(
    'attending_physician', metadata,
    Column('d_name', String(35)),
    Column('d_patronymic', String(35)),
    Column('d_surname', String(35)),
    Column('start_medical_examination', Time),
    Column('end_medical_examination', Time),
    Column('fk_patient_id', ForeignKey('medication.patient.patient_id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, unique=True),
    schema='medication'
)


t_delivery_pills = Table(
    'delivery_pills', metadata,
    Column('ward', Integer),
    Column('delivered', Boolean),
    Column('time_delivery', DateTime(True)),
    Column('fk_nurse_id', ForeignKey('medication.duty_list.nurse_id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True),
    Column('fk_patient_id', ForeignKey('medication.patient.patient_id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True),
    schema='medication'
)


t_diagnosis = Table(
    'diagnosis', metadata,
    Column('provisional_diagnosis', String(255)),
    Column('refined_diagnosis', String(255)),
    Column('date_of_diagnosis', Date),
    Column('dynamics', String(255)),
    Column('fk_patient_id', ForeignKey('medication.patient.patient_id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, unique=True),
    schema='medication'
)


class DutyList(Base):
    __tablename__ = 'duty_list'
    __table_args__ = {'schema': 'medication'}

    nurse_id = Column(Integer, primary_key=True, server_default=text("nextval('"medication".duty_list_nurse_id_seq'::regclass)"))
    nurse_name = Column(String(100))
    start_shift = Column(Time)


class Mark(Base):
    __tablename__ = 'mark'
    __table_args__ = {'schema': 'medication'}

    cell_id = Column(BigInteger, primary_key=True)
    identifier = Column(String(255), nullable=False, unique=True)
    switch = Column(Boolean)
    fk_patient_id = Column(ForeignKey('medication.patient.patient_id', ondelete='RESTRICT', onupdate='RESTRICT'), unique=True)

    fk_patient = relationship('Patient')


class Patient(Base):
    __tablename__ = 'patient'
    __table_args__ = {'schema': 'medication'}

    patient_id = Column(BigInteger, primary_key=True, server_default=text("nextval('"medication".patient_patient_id_seq'::regclass)"))
    p_name = Column(String(35))
    p_patronymic = Column(String(35))
    p_surname = Column(String(35))
    birth_date = Column(Date)
    medical_policy = Column(String(16))
    contact_phone = Column(String(11))
    type_hospitalization = Column(String(25))
    date_hospitalization = Column(Date)
    discharged = Column(Boolean)


class PrescribedMedication(Base):
    __tablename__ = 'prescribed_medication'
    __table_args__ = {'schema': 'medication'}

    enumerator = Column(BigInteger, primary_key=True, server_default=text("nextval('"medication".prescribed_medication_enumerator_seq'::regclass)"))
    drug_name = Column(String(255))
    fk_patient_id = Column(ForeignKey('medication.patient.patient_id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True)

    fk_patient = relationship('Patient')


class TreatmentDepartment(Base):
    __tablename__ = 'treatment_department'
    __table_args__ = {'schema': 'medication'}

    branch_id = Column(Integer, primary_key=True, server_default=text("nextval('"medication".treatment_department_branch_id_seq'::regclass)"))
    floor = Column(SmallInteger)
    branch_name = Column(String(35))
    department_head = Column(String(100))
    head_nurse = Column(String(100))
    station_phone = Column(String(11))


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'medication'}

    id = Column(BigInteger, primary_key=True, server_default=text("nextval('"medication".users_id_seq'::regclass)"))
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(BigInteger, nullable=False)


t_ward = Table(
    'ward', metadata,
    Column('ward', Integer),
    Column('ward_capacity', SmallInteger),
    Column('position', SmallInteger),
    Column('fk_patient_id', ForeignKey('medication.patient.patient_id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, unique=True),
    Column('fk_branch_id', ForeignKey('medication.treatment_department.branch_id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True),
    schema='medication'
)
