from sqlalchemy import create_engine
class DbUtils:
	#db_string = "postgresql+psycopg2://admin:admin@localhost/postgres"
	POSTGRES_URL="127.0.0.1:5432"
	POSTGRES_USER="postgres"
	POSTGRES_PW="root"
	POSTGRES_DB="test"
	
	db_string ='postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
	def createTable(self):
		db = create_engine(self.db_string)
		db.execute("CREATE TABLE IF NOT EXISTS users (username text, password text, email text)")
	
	def addNewUser(self,username, password, email):
		db = create_engine(self.db_string)
		db.execute("INSERT INTO users(username, password, email) VALUES (%s,%s, %s)", username, password, email)  
	
	def getUsers(self):  
		db = create_engine(self.db_string)
		users = db.execute("SELECT * FROM users")
		return users