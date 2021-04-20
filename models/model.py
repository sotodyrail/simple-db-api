from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy as sqlalchemy

db = sqlalchemy(app)
db.init_app(app)


class BaseModel(db.Model):
    """
    Base model class tyhat provides RMQ notify
    """

    def notify(self):
        """
        RMQ notify
        :return: bool result
        """
        pass
