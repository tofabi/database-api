from database_api.database_control import database_control
import database_api.statuscodes
import json


default_localhost = "host='localhost' dbname='postgres' user='postgres'"
database_variable = 'DATABASE_URL'
database = database_control(database_variable,default_localhost)


if __name__ == '__main__':
    status = database.connect()

