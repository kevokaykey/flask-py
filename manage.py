from flask_script import Manager

#local import
from database import Database

#create databse instance
db = Database()

app = Flask(__name__) # flask app instance

#manager requires a flask instance
manager = Manager(app)

@manager.command
def create_db():
    db.create_tables()

@manager.command
def drop_db():
    db.drop_table()    


if __name__ == '__main__'
manager.run()


