import psycopg2
import os
import json
from .statuscodes import *

class database_api(object):
    default_localhost = None
    database_url = None
    conn = None
    cur = None

    #Object init with environment variable to database and default localhost url
    def __init__(self, database_variable, default_localhost):
        self.default_localhost = default_localhost
        self.database_url = os.environ.get(database_variable, default_localhost)

    # Try to connect to database
    # Use different mode for localhost
    def connect(self):
        if self.database_url == self.default_localhost:
            self.conn = psycopg2.connect(self.database_url)
        else:
            self.conn = psycopg2.connect(self.database_url, sslmode='require')
        self.cur = self.conn.cursor()
        if self.cur is None or self.conn is None:
            return {'status':ERROR_NOT_CONNECTED}
        else:
            return{'status':OK}

    # Try to close the connection if it exist
    def disconnect(self):
        if(self.cur != None):
            self.cur.close()
            self.cur = None
        if(self.conn != None):
            self.conn.close()
            self.conn = None
        return{'status':OK}

    #Execute a SQL command
    # If no parameters are required set it to None
    # If the command change content of the database commit have to be set to true, otherwise to false
    def executeCommand(self, command, parameter, commit):
        if (self.conn is not None) and (self.cur is not None):
            try:
                if parameter == None:
                    self.cur.execute(command)
                else:
                    self.cur.execute(command, parameter)
                if commit:
                    self.conn.commit()
                status = {'status': OK}
                return status
            except Exception as e:
                error = {'status': ERROR_EXECUTE, 'exception':e}
                return error
        else:
            error = {'status': ERROR_NOT_CONNECTED}
            return error

    #Create a Table user_table if it not exist
    def createUserTable(self):
        command = """CREATE TABLE IF NOT EXISTS user_table (
                    user_name name PRIMARY KEY,
                    chat_id name,
                    rights name
                    )"""
        status = self.executeCommand(command, None, True)
        return status

    #Create a Table device_table if it not exist
    def createDeviceTable(self):
        command = """CREATE TABLE IF NOT EXISTS device_table (
                    device_name name PRIMARY KEY,
                    device_typ name,
                    device_location name,
                    home name,
                    FOREIGN KEY (home) REFERENCES home_table (home_name),
                    device_owner name,
                    FOREIGN KEY (device_owner) REFERENCES user_table (user_name),
                    device_friends name ARRAY
                    )"""
        status = self.executeCommand(command, None, True)
        return status

    #Create a Table home_table if it not exist
    def createHomeTable(self):
        command = """CREATE TABLE IF NOT EXISTS home_table (
                    home_name name PRIMARY KEY,
                    gateway_ip name,
                    home_owner name,
                    FOREIGN KEY (home_owner) REFERENCES user_table (user_name),
                    home_friends name ARRAY
                    )"""
        status = self.executeCommand(command, None, True)
        return status

    #Check if a user with the given chat_id exist in the database
    def exist_user(self, user):
        if 'user_name' in user:
            command = """SELECT chat_id FROM user_table WHERE user_name = %s"""
            parameter = user['user_name'],
            status = self.executeCommand(command, parameter, False)
        else:
            command = """SELECT user_name FROM user_table WHERE chat_id = %s"""
            parameter = user['chat_id'],
            status = self.executeCommand(command, parameter, False)
        if status['status'] == OK:
            if self.cur.fetchone() is None:
                status =  {'status':OK, 'result': 'False'}
                return status
            else:
                status = {'status':OK, 'result':'True'}
                return status
        else:
            return status
        
    #Add a new user to the user_table
    def add_user(self, parameter):
        print(parameter)
        command = """INSERT INTO user_table(user_name, chat_id) VALUES(%s,%s)"""
        command_parameter = parameter['user_name'], parameter['chat_id']
        status = self.executeCommand(command, command_parameter, True)
        return status

    #Delete a user from user_table
    def delete_user(self, parameter):
        command = "DELETE FROM user_table WHERE chat_id = %s"
        command_parameter = parameter['chat_id'],
        status = self.executeCommand(command, command_parameter, True)
        return status
    
    #Add a new home to the home_table
    def add_home(self, parameter):
        command ="""INSERT INTO home_table(home_name, gateway_ip, home_owner) 
                   VALUES(%s,%s,(SELECT user_name FROM user_table WHERE chat_id= %s))"""
        command_parameter = parameter['home_name'],parameter['gateway_ip'], parameter['chat_id'],
        status = self.executeCommand(command, command_parameter, True)
        return status

    #Delete a home from home_table
    def delete_home(self, parameter):
        command = "DELETE FROM home_table WHERE home_name = %s"
        command_parameter = parameter['home_name'],
        status = self.executeCommand(command, command_parameter, True)
        return status

    #Add a new device to the device_table
    def add_device(self, parameter):
        command = """INSERT INTO device_table
                 (device_name, device_typ, device_location, home, device_owner)
                 VALUES(%s,%s,%s,(SELECT home_name FROM home_table WHERE home_name = %s),(SELECT user_name FROM user_table WHERE chat_id = %s))"""
        command_parameter = parameter['device_name'],parameter['device_typ'],parameter['device_location'],parameter['home_name'],parameter['chat_id'],
        status = self.executeCommand(command, command_parameter, True)
        return status
    
    #Delete a device from the device_table
    def delete_device(self, parameter):
        command = """DELETE FROM device_table WHERE device_name = %s"""
        command_parameter = parameter['device_name'],
        status = self.executeCommand(command, command_parameter, True)
        return status

    #Add a friend to a home
    def add_friend_home(self, parameter):
        command = """UPDATE home_table SET
                    home_friends = array_append(home_friends, %s)
                    WHERE home_name = %s"""
        command_parameter = parameter['home_friends'],parameter['home_name'],
        status = self.executeCommand(command, command_parameter,True)
        return status

    #Delete a friend from a home
    def delete_friend_home(self, parameter):
        command = """UPDATE home_table SET
                    home_friends = array_remove(home_friends, %s)
                    WHERE home_name = %s"""
        command_parameter = parameter['home_friends'],parameter['home_name'],
        status = self.executeCommand(command, command_parameter,True)
        return status
    
    #Add a friend to a device
    def add_friend_device(self, parameter):
        command = """UPDATE device_table SET
                    device_friends = array_append(device_friends, %s)
                    WHERE device_name = %s"""
        command_parameter = parameter['device_friends'],parameter['device_name']
        status = self.executeCommand(command, command_parameter,True)
        return status

    #Delete a friend from a device
    #First check if device exit and user has permission
    def delete_friend_device(self, parameter):
        command = """UPDATE device_table SET
                    device_friends = array_remove(device_friends, %s)
                    WHERE device_name = %s"""
        command_parameter = parameter['device_friends'],parameter['device_name']
        status = self.executeCommand(command, command_parameter,True)
        return status

    def get_from_user_table(self, parameter, request):
        command = "SELECT "
        first = True
        for pars in request:
            if first:
                command += pars
                first = False
            else:
                command += "," + pars
        
        command += """ FROM user_table """
        command_parameter = []
        first = True
        for key in parameter:
            if first:
                first = False
                command +="WHERE "
            else:
                command +="AND "
            command += key + " = %s "
            command_parameter.append(parameter[key])
        command_parameter = tuple(command_parameter)
        
        status = self.executeCommand(command, command_parameter, False)
        if status['status'] == OK:
            row = self.cur.fetchone()
            array = []
            while(row is not None):
                array.append(row)
                row = self.cur.fetchone()
            status['result'] = array
            return status
        else:
            return status

    def get_from_home_table(self, parameter, request):
        command = "SELECT "
        first = True
        for pars in request:
            if first:
                command += pars
                first = False
            else:
                command += "," + pars
        
        command += """ FROM home_table
                        INNER JOIN user_table ON user_table.user_name = home_table.home_owner """
        command_parameter = []
        first = True
        for key in parameter:
            if first:
                first = False
                command +="WHERE "
            else:
                command +="AND "
            if key == 'home_friends':
                command += "%s = ANY(home_table.home_friends) "
            else:
                command += key + " = %s "
            command_parameter.append(parameter[key])
        command_parameter = tuple(command_parameter)
        status = self.executeCommand(command, command_parameter, False)
        if status['status'] == OK:
            row = self.cur.fetchone()
            array = []
            while(row is not None):
                array.append(row)
                row = self.cur.fetchone()
            status['result'] = array
            return status
        else:
            return status

    def get_from_device_table(self, parameter, request):
        command = "SELECT "
        first = True
        for pars in request:
            if first:
                command += pars
                first = False
            else:
                command += "," + pars
        
        command += """ FROM device_table
                        INNER JOIN user_table ON user_table.user_name = device_table.device_owner 
                        INNER JOIN home_table ON home_table.home_name = device_table.home """
        command_parameter = []
        first = True
        for key in parameter:
            if first:
                first = False
                command +="WHERE "
            else:
                command +="AND "
            if key == 'device_friends':
                command += "%s = ANY(device_table.device_friends) "
            else:
                command += key + " = %s "
            command_parameter.append(parameter[key])
        command_parameter = tuple(command_parameter)
        status = self.executeCommand(command, command_parameter, False)
        if status['status'] == OK:
            row = self.cur.fetchone()
            array = []
            while(row is not None):
                array.append(row)
                row = self.cur.fetchone()
            status['result'] = array
            return status
        else:
            return status
