from flask import Flask
from flask_admin import Admin
from flask_admin.contrib import sqla
from api.v1 import routes

app = Flask(__name__)
app.config.from_object('settings.config.Config')
app.register_blueprint(routes.medication_repo)


with app.app_context():
    from models.medication_models import Ward, User, TreatmentDepartment, PrescribedMedication, Patient, Mark, Diagnosis, DeliveryPill, AttendingPhysician, DutyList, db
    from safrs import SAFRSAPI

    api = SAFRSAPI(app, host='localhost', port=5001, prefix="")
    admin = Admin(app, url="/admin")
    for cls in (Ward, User, TreatmentDepartment, PrescribedMedication, Patient, Mark, Diagnosis, DeliveryPill, AttendingPhysician, DutyList):
        print(cls.__name__)
        api.expose_object(cls)
        admin.add_view(sqla.ModelView(cls, db.session))
