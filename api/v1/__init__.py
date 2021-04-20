from flask import Blueprint
from settings.endpoint import api_v1

medication_repo = Blueprint('medication_repo', __name__, url_prefix=api_v1)