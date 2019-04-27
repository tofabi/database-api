from database_api.database_control import database_control
import database_api.statuscodes
import json
import pika
import os
import time
import json
from rabbit_connector import AMQPServer

default = "http://localhost:5672"
url = os.environ.get('CLOUDAMQP_URL', default)
print(url)
params = pika.URLParameters(url)


default_localhost = "host='localhost' dbname='postgres' user='postgres'"
database_variable = 'DATABASE_URL'

def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True

def check_payload(payload, request):
    if not is_json(payload):
        print("no json")
        return False
    payload = json.loads(payload)
    print("paramter")
    if not 'chat_id' in payload:
        return False
    if not 'parameter' in payload:
        return False
    if request:
        if not 'request' in payload:
            return False
    return True


def setup_listener():
    global server
    server.channel.exchange_declare(exchange="db_exchange", exchange_type="topic", durable=True)
    server.channel.queue_declare(queue='db_user')
    server.channel.queue_declare(queue='db_home')
    server.channel.queue_declare(queue='db_device')
    server.channel.queue_bind(queue="db_user", exchange="db_exchange", routing_key="user.*")
    server.channel.queue_bind(queue="db_home", exchange="db_exchange", routing_key="home.*")
    server.channel.queue_bind(queue="db_device", exchange="db_exchange", routing_key="device.*")

    @server.register('db_user', sync=True)
    def user(res):
        routing_key = res['routing_key']
        payload = res['body']
        print(payload)
        if check_payload(payload, False):
            payload = json.loads(payload)
            chat_id = payload['chat_id']
            parameter = payload['parameter']

            command = routing_key.split('.')

            if (command[1] == "add"):
                database = database_control(database_variable, default_localhost);
                database.connect()
                result = database.add_user(chat_id, parameter)
                return json.dumps(result)

            elif command[1] == "delete":
                database = database_control(database_variable, default_localhost);
                database.connect()
                result = database.delete_user(chat_id, parameter)
                return json.dumps(result)

            elif command[1] == "exist":
                database = database_control(database_variable, default_localhost);
                database.connect()
                result = database.exist_user(chat_id, parameter)
                return json.dumps(result)

            else:
                status = {'status': database_api.statuscodes.ERROR_UNKNOWN_COMMAND}
                return json.dumps(status)
        else:
            status = {'status': database_api.statuscodes.ERROR_WRONG_PAYLOAD}
            return json.dumps(status)

    @server.register('db_home', sync=True)
    def home(res):
        routing_key = res['routing_key']
        payload = res['body']
        if check_payload(payload, False):
            payload = json.loads(payload)
            chat_id = payload['chat_id']
            parameter = payload['parameter']

            command = routing_key.split('.')

            if (command[1] == "add"):
                database = database_control(database_variable, default_localhost);
                database.connect()
                result = database.add_home(chat_id, parameter)
                return json.dumps(result)

            elif command[1] == "delete":
                database = database_control(database_variable, default_localhost);
                database.connect()
                result = database.delete_home(chat_id, parameter)
                return json.dumps(result)

            elif command[1] == "get":
                if check_payload(payload, True):
                    request = payload['request']
                    database = database_control(database_variable, default_localhost);
                    database.connect()
                    result = database.get_home(chat_id, parameter, request)
                    return json.dumps(result)
                else:
                    status = {'status': database_api.statuscodes.ERROR_WRONG_PAYLOAD}
                    return status

            elif command[1] == "add_friend":
                database = database_control(database_variable, default_localhost);
                database.connect()
                result = database.add_friend_home(chat_id, parameter)
                return json.dumps(result)

            elif command[1] == "delete_friend":
                database = database_control(database_variable, default_localhost);
                database.connect()
                result = database.delete_friend_home(chat_id, parameter)
                return json.dumps(result)

            else:
                status = {'status': database_api.statuscodes.ERROR_UNKNOWN_COMMAND}
                return json.dumps(status)
        else:
            status = {'status': database_api.statuscodes.ERROR_WRONG_PAYLOAD}
            return json.dumps(status)

    @server.register('db_device', sync=True)
    def device(res):
        routing_key = res['routing_key']
        payload = res['body']
        if check_payload(payload, False):
            payload = json.loads(payload)
            chat_id = payload['chat_id']
            parameter = payload['parameter']

            command = routing_key.split('.')

            if (command[1] == "add"):
                database = database_control(database_variable, default_localhost);
                database.connect()
                result = database.add_device(chat_id, parameter)
                return json.dumps(result)

            elif command[1] == "delete":
                database = database_control(database_variable, default_localhost);
                database.connect()
                result = database.delete_device(chat_id, parameter)
                return json.dumps(result)

            elif command[1] == "get":
                if check_payload(payload, True):
                    request = payload['request']
                    database = database_control(database_variable, default_localhost);
                    database.connect()
                    result = database.get_device(chat_id, parameter, request)
                    return json.dumps(result)
                else:
                    status = {'status': database_api.statuscodes.ERROR_WRONG_PAYLOAD}
                    return status

            elif command[1] == "add_friend":
                database = database_control(database_variable, default_localhost);
                database.connect()
                result = database.add_friend_device(chat_id, parameter)
                return json.dumps(result)

            elif command[1] == "delete_friend":
                database = database_control(database_variable, default_localhost);
                database.connect()
                result = database.delete_friend_device(chat_id, parameter)
                return json.dumps(result)

            else:
                status = {'status': database_api.statuscodes.ERROR_UNKNOWN_COMMAND}
                return json.dumps(status)
        else:
            status = {'status': database_api.statuscodes.ERROR_WRONG_PAYLOAD}
            return json.dumps(status)

if __name__ == '__main__':
    global server
    connection = pika.BlockingConnection(params)
    server = AMQPServer(connection)

    setup_listener()

    server.start_listening()

    while True:
        time.sleep(5)
        

    server.disconnect()


