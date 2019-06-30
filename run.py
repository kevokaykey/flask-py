from flask import Flask
from app import mod


app = Flask(__name__)

app.register_blueprint(mod, url_prefix="/example") #register blueprint

if __name__ == '__main__':
    app.run()