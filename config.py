import os
basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://riset1231:riset1231@c02.cxhy9bpkxdlw.us-west-2.rds.amazonaws.com:3306/co2'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
