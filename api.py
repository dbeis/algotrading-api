import os
from flask import Flask



app = Flask('algotrading-api', instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
    #DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)

from controllers import install_controllers
install_controllers(app, '/api')

# leave this for testing whatever
@app.route('/')
def hello():
    return 'index :)'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True)