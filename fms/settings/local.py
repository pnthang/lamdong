#import os

from .base import *

# Example configuration
DEBUG = True
POSTGRES_URL="192.168.100.121:5432"
POSTGRES_USER="postgres"
POSTGRES_PW="Inno@2018"
POSTGRES_DB="geoinno"

DATABASE_URI ='postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)

SECRET_KEY = "8a3971a57fea4db08d86aa844e8ecefe"
JWT_SECRET_KEY = "8a3971a57fea4db08d86aa844e8ecefe"

UPLOAD_FOLDER = 'C:\\Temp\\fms'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])