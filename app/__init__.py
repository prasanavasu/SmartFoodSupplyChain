from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
db = SQLAlchemy(app)
app.secret_key = 'Hackthon'
cors = CORS(app)

from app.views import *

with app.app_context():
    db.create_all()