# Secret key for generating tokens
SECRET_KEY='xu4oGFjn1_6PkiydrZitCE9JIozEZv3jMrvHl0T66Pk'
SECURITY_PASSWORD_SALT='250411626211731261460976096525945109056'

# Database configuration
# SQLALCHEMY_DATABASE_URI='postgresql://postgres@localhost:5432/sms'
SQLALCHEMY_DATABASE_URI='postgres://default:7ZYwLXap4xlP@ep-raspy-lake-a4ot0dgi-pooler.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require'
# SQLALCHEMY_DATABASE_URI='postgresql://postgres:QsdQEVlCuBeuBcCmiHzXOTkkAESSNGzi@postgres.railway.internal:5432/railway'
SQLALCHEMY_TRACK_MODIFICATIONS=False
SQLALCHEMY_ENGINE_OPTIONS={"pool_pre_ping": True,}

#Registration
SECURITY_REGISTERABLE=True
SECURITY_CONFIRMABLE=True

#Recover/reset
SECURITY_RECOVERABLE=True

#Cookie settings
REMEMBER_COOKIE_SAMESITE='strict'
SESSION_COOKIE_SAMESITE='strict'

#Mail settings
MAIL_SERVER='smtp.gmail.com'
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME = 'chatelobenna@gmail.com'
MAIL_PASSWORD = 'dcyuxrnsqyzhazqj'
MAIL_DEFAULT_SENDER = 'nyiganetabkalenjin@gmail.com'

SECURITY_CHANGE_EMAIL=True