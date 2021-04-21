class Config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/medication'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SESSION_TYPE = 'filesystem'
