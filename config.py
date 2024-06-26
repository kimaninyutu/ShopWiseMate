
class Config:
    SECRET_KEY = 'kimaninyutu'
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'


class ProductionConfig(Config):
    DEBUG = False
    ENV = 'production'
