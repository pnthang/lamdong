from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from fms import app

engine = create_engine(app.config['DATABASE_URI'], convert_unicode=True,echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
	Base.metadata.create_all(bind=engine)

@app.teardown_request
def shutdown_session(exception=None):
	db_session.remove()
	
@app.after_request
def after_request(response):
	db_session.remove()
	return response
