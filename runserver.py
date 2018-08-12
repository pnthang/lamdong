#import os
from fms import app
from fms.database import init_db

init_db()
if __name__ == "__main__":
	app.run()
