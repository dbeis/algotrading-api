import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask('algotrading-api', instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
    SQLALCHEMY_DATABASE_URI="sqlite:////tmp/test.db"
)

db = SQLAlchemy(app)
from entities import *
db.create_all()

from controllers import install_controllers
install_controllers('/api')

# leave this for testing whatever
@app.route('/')
def hello():
    return 'index :)'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True)