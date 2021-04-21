from flask import Flask
from flask_admin import Admin
from flask_admin.contrib import sqla
from api.v1 import routes

app = Flask(__name__)
app.config.from_object('settings.config.Config')
app.register_blueprint(routes.medication_repo)
app.secret_key = 'secret key'

with app.app_context():
    from models.medication_models import Drug, DutyList, Patient, TreatmentDepartment, AttendingPhysician, DeliveryPill, Diagnosis, Mark, PrescribedMedication, Ward, Attached, db
    from safrs import SAFRSAPI

    api = SAFRSAPI(app, host='localhost', port=5000, prefix="")
    admin = Admin(app, url="/admin", template_mode='bootstrap3')
    for cls in (Drug, DutyList, Patient, TreatmentDepartment, AttendingPhysician, DeliveryPill, Diagnosis, Mark, PrescribedMedication, Ward, Attached):
        print(cls.__name__)
        api.expose_object(cls)
        admin.add_view(sqla.ModelView(cls, db.session))
