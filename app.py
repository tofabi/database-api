from flask import Flask, request
from database_api.database_control import database_control
import database_api.statuscodes
import json


default_localhost = "host='localhost' dbname='tobias' user='tobias'"
database_variable = 'self.database_URL'
database = database_control(database_variable,default_localhost)

app = Flask(__name__)

def shutdown_server():
    database.disconnect()
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown')
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

@app.route('/')
def hello_world():
    status = database.add_home('345',{'home_name':'app','gateway_ip':'789'})
    return json.dumps(status)

if __name__ == '__main__':
    status = database.connect()
    print(status)
    print(database.add_user('345',{'user_name':'server'}))
    app.run()

