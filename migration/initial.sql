
DROP SCHEMA medication CASCADE;
CREATE SCHEMA medication;

CREATE TABLE patient 
( 
	id SERIAL PRIMARY KEY,
	p_name VARCHAR(35), 
	p_patronymic VARCHAR(35), 
	p_surname VARCHAR(35), 
	birth_date DATE,
	medical_policy VARCHAR(17), 
	contact_phone VARCHAR(12), 
	type_hospitalization VARCHAR(25),
	date_hospitalization DATE, 
	discharged BOOLEAN
);
CREATE TABLE treatment_department 
(
	id SERIAL PRIMARY KEY,
	storey BOOLEAN, 
	branch_name VARCHAR(35), 
	department_head VARCHAR(100), 
	head_nurse VARCHAR(100), 
	station_phone VARCHAR(11)
);
CREATE TABLE ward 
(
	id SERIAL PRIMARY KEY,
	ward_capacity SMALLINT CHECK (ward_capacity > 0),
	branch_id INTEGER NOT NULL, 
	CONSTRAINT fk_branch_id FOREIGN KEY (branch_id) REFERENCES treatment_department(id) ON DELETE SET NULL
);
CREATE TABLE attached
(
	id SERIAL PRIMARY KEY,
	patient_id INTEGER NOT NULL UNIQUE,
	ward_id INTEGER NOT NULL,
	place SMALLINT CHECK (place > 0),
	CONSTRAINT fk_ward_id FOREIGN KEY (ward_id) REFERENCES ward(id),
	CONSTRAINT fk_patient_id FOREIGN KEY (patient_id) REFERENCES patient(id) ON DELETE CASCADE
);

CREATE TABLE drug 
(
	id SERIAL PRIMARY KEY,
	drug_name VARCHAR(255)
);
CREATE TABLE prescribed_medication 
(
	id SERIAL PRIMARY KEY,
	patient_id INTEGER NOT NULL,
	drug_id INTEGER,
	CONSTRAINT fk_patient_id FOREIGN KEY (patient_id) REFERENCES patient(id) ON DELETE CASCADE,
	CONSTRAINT fk_drug_id FOREIGN KEY (drug_id) REFERENCES drug(id)
);
CREATE TABLE attending_physician
(
	id SERIAL PRIMARY KEY,
	d_name VARCHAR(35), 
	d_patronymic VARCHAR(35),
	d_surname VARCHAR(35), 
	start_medical_examination TIME, 
	end_medical_examination TIME,
	patient_id INTEGER NOT NULL, 
	CONSTRAINT fk_patient_id FOREIGN KEY (patient_id) REFERENCES patient(id)
);
CREATE TABLE duty_list 
( 
	id SMALLSERIAL PRIMARY KEY, 
	nurse_name VARCHAR(100), 
	start_shift TIME
);
CREATE TABLE delivery_pills 
(
	id SERIAL PRIMARY KEY,
	nurse_id INTEGER,
	patient_id INTEGER,
	delivered BOOLEAN, 
	time_delivery DATE, 
	CONSTRAINT fk_nurse_id FOREIGN KEY (nurse_id) REFERENCES duty_list(id),
	CONSTRAINT fk_patient_id FOREIGN KEY (patient_id) REFERENCES patient(id)
);
CREATE TABLE diagnosis 
(
	id SERIAL PRIMARY KEY,
	provisional_diagnosis VARCHAR(255),
	refined_diagnosis VARCHAR(255),
	date_of_diagnosis DATE,
	dynamics VARCHAR(255),
	patient_id INTEGER NOT NULL UNIQUE,
	CONSTRAINT fk_patient_id FOREIGN KEY (patient_id) REFERENCES patient(id) ON DELETE CASCADE
);

CREATE TABLE mark
(
	id SERIAL PRIMARY KEY,
	identifier INTEGER NOT NULL UNIQUE,
	switch BOOLEAN DEFAULT False,
	patient_id INTEGER NOT NULL UNIQUE, 
	CONSTRAINT fk_patient_id FOREIGN KEY (patient_id) REFERENCES patient(id)
);
