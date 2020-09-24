import os
import pymysql
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "sdq34dfhfj#%#fsgser#@#"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Setting Cognito
    REGION = 'us-west-2'
    USERPOOL_ID = ''
    APP_CLIENT_ID = ''
    APP_CLIENT_SECRET = ''
    COGNITO_SCOPE='email+openid+phone'
    KEYS_URL = 'https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json'.format(REGION, USERPOOL_ID)

    # AWS CREDENTIALS
    AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY') or ''
    AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY') or ''


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    LOGIN_DISABLED = True