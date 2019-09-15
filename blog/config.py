import os
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class Base_Config():
    SECRET_KEY = os.getenv('SECRET_KEY','secret string')

    SQLALCHEMY_TRACK_MODIFICATIONS = False #关闭变量追踪

    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('Blog Admin',MAIL_USERNAME)
    ##
    BLUELOG_EMAIL = os.getenv('BLUELOG_EMAIL')
    BLUELOG_POST_PER_PAGE = 10
    BLUELOG_MANAGE_POST_PER_PAGE = 15
    BLUELOG_COMMENT_PER_PAGE = 15

class Development_Config(Base_Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'data-dev.db')

class TestingConfig(Base_Config):
    TESTING = True
    WTF_CSRF_ENABLE = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class Producion_Config(Base_Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL','sqlite:///'+os.path.join(basedir,'data.db'))
    #生产环境下数据库URL 通常从环境变量中读取 更健壮的DBMS

config = {
    'development' : Development_Config,
    'testing' : TestingConfig,
    'production' : Producion_Config,
}



