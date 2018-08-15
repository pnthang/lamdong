DEBUG = False

POSTGRES_URL="127.0.0.1:5432"
POSTGRES_USER="postgres"
POSTGRES_PW="Inno@2018"
POSTGRES_DB="test"

DATABASE_URI ='postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
#DATABASE_URI = 'sqlite:////tmp/development.db'

SECRET_KEY = "8a3971a57fea4db08d86aa844e8ecefe"

UPLOAD_FOLDER = '/tmp/fms'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])