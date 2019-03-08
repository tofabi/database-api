# database_control
#This class especially check if the reqeusts are allowed and the user is authorized
#To get and modify data it use the database_api

from .database_api import database_api
import json
from .statuscodes import *
from copy import deepcopy



class database_control(object):
    database = None

    #Creates the database_api object
    def __init__(self, database_variable, default_localhost):
        self.database = database_api(database_variable, default_localhost)

    #Connect the databse_api to the database
    def connect(self):
        response = self.database.connect()
        if response['status'] is OK:
            print('connect')
            status = self.database.createUserTable()
            print(status)
            status = self.database.createHomeTable()
            print(status)
            status = self.database.createDeviceTable()
            print(status)
            return response
        else:
            return response

    #Disconnect the database_api from the database
    def disconnect(self):
        return self.database.disconnect()

    def exist_user(self, chat_id, parameter):
        requiered_parameter = []
        optional_parameter = ['user_name']
        parameter = self.check_parameter(parameter, requiered_parameter, optional_parameter)
        if parameter is None:
            error = {'status':ERROR_PARAMETER_NOT_VALID} 
            return error
        parameter['chat_id'] = chat_id
        return self.database.exist_user(parameter)

    #Call the funktion to add a user if in the request is everything fine
    def add_user(self, chat_id, parameter):
        #Check if the parameters are valid
        requiered_parameter = ['user_name']
        optional_parameter = []
        parameter = self.check_parameter(parameter, requiered_parameter, optional_parameter)
        if parameter is None:
            error = {'status':ERROR_PARAMETER_NOT_VALID} 
            return error
        
        #Check if the user_name already exist
        result = self.database.get_from_user_table(parameter, ['chat_id'])
        if result['status'] is not OK:
            return result
        if len(result['result']) >0:
            error ={'status':ERROR_NAME_ALREADY_EXIST}
            return error
        
        #Create user
        parameter['chat_id'] = chat_id
        parameter['rights'] = 'standard'
        result = self.database.add_user(parameter)
        return result

    #Delete a user if in the request everything is fine
    def delete_user(self, chat_id, parameter):
        #Check if the parameters are valid
        requiered_parameter = []
        optional_parameter = ['user_name']
        parameter = self.check_parameter(parameter, requiered_parameter, optional_parameter)
        if parameter is None:
            error = {'status':ERROR_PARAMETER_NOT_VALID}
            return error
        
        #Check if the user exist
        result = self.database.get_from_user_table({'chat_id':chat_id}, ['user_name','rights'])
        if result['status'] is not OK:
            return result
        if len(result['result']) == 0:
            error = {'status':ERROR_NOT_EXIST}
            return error
        
        #Check if the user want to delete himself
        if parameter['user_name'] == None:
            #Delete user
            result2 = self.database.delete_user({'user_name':result['result'][0][0]})
            return result2
        
        #Check if the user is allowed to delete other users
        if not(result['result'][0][1] == 'admin'):
            error = {'status':ERROR_NO_PERMISSION}
            return error

        #Delete user a admin
        result = self.database.delete_user(parameter)
        return result
            
    #Add a home if the in the request everything is fine
    def add_home(self, chat_id, parameter):
        #Check if the parameters are valid
        requiered_parameter = ['home_name','gateway_ip']
        optional_parameter = []
        parameter = self.check_parameter(parameter, requiered_parameter, optional_parameter)
        if parameter is None:
            error = {'status':ERROR_PARAMETER_NOT_VALID}
            return error

        #Check if home already exist
        result = self.database.get_from_home_table({'home_name':parameter['home_name']}, ['gateway_ip'])
        if result['status'] is not OK:
            return result
        if len(result['result']) >0:
            error = {'status':ERROR_NAME_ALREADY_EXIST}
            return error
        
        #Create new home
        parameter['chat_id'] = chat_id
        result = self.database.add_home(parameter)
        return result

    #Delete a home if in the reqeust everything is fine
    def delete_home(self,chat_id, parameter):
        #Check if the parameters are valid
        requiered_parameter = []
        optional_parameter = []
        parameter = self.check_parameter(parameter, requiered_parameter, optional_parameter)
        if parameter is None:
            error = {'status':ERROR_PARAMETER_NOT_VALID}
            return error

        #Check if the home exist
        result = self.database.get_from_home_table({'home_name':parameter['home_name']}, ['chat_id'])
        if result['status'] is not OK:
            return result
        if len(result['result']) == 0:
            error = {'status':ERROR_NOT_EXIST}
            return error
        
        #Check if the user is allowed to delete the home
        if not(chat_id == result['result'][0][0]):
            #Check if the user has admin rights
            result = self.database.get_from_user_table({'chat_id':chat_id}, ['rights'])
            if result['status'] is not OK:
                return result
            if not(result['result'][0][0] == 'admin'):
                error = {'status':ERROR_NO_PERMISSION}
                return error
            
        #Delete the home as admin
        result = self.database.delete_home(parameter)
        return result

    #Add a device if the request is fine
    def add_device(self,chat_id, parameter):
        #Check if the parameters are valid
        requiered_parameter = ['device_name','device_typ','device_location','home_name']
        optional_parameter = []
        parameter = self.check_parameter(parameter, requiered_parameter, optional_parameter)
        if parameter is None:
            error = {'status':ERROR_PARAMETER_NOT_VALID}
            return error

        #Check if device already exist
        result = self.database.get_from_device_table({'device_name':parameter['device_name']}, ['home_name'])
        if result['status'] is not OK:
            return result
        if len(result['result']) >0:
            error = {'status':ERROR_NAME_ALREADY_EXIST}
            return error

        #Check if the user is allowed to create a device in the home
        user = self.database.get_from_user_table({'chat_id':chat_id},['user_name'])
        if result['status'] is not OK:
            return result
        result = self.database.get_from_home_table({'home_name':parameter['home_name']}, ['home_owner','home_friends'])
        if result['status'] is not OK:
            return result
        if len(result['result']) == 0:
            error = {'status':ERROR_HOME_NOT_EXIST}
            return error
        if not ((result['result'][0][0] == user['result'][0][0]) or (user['result'][0][0] in result['result'][0][1])):
            error = {'status':ERROR_NO_PERMISSION}
            return error
        
        #Create new device
        parameter['chat_id'] = chat_id
        result = self.database.add_device(parameter)
        return result

    #Delete a device if in the reqeust is all right
    def delete_device(self,chat_id, parameter):
        #Check if parameters are valid
        requiered_parameter = ['device_name']
        optional_parameter = []
        parameter = self.check_parameter(parameter, requiered_parameter, optional_parameter)
        if parameter is None:
            error = {'status':ERROR_PARAMETER_NOT_VALID}
            return error
        
        #Check if the device exist
        result = self.database.get_from_device_table({'device_name':parameter['device_name']},['chat_id'])
        if result['status'] is not OK:
            return result
        if len(result['result']) == 0:
            error = {'status':ERROR_NOT_EXIST}
        
        #Check if the user has the permission to delete the device
        if not(chat_id == result['result'][0][0]):
            #Check if the user has admin rights
            result = self.database.get_from_user_table({'chat_id':chat_id}, ['rights'])
            if result['status'] is not OK:
                return result
            if not(result['result'][0][0] == 'admin'):
                error = {'status':ERROR_NO_PERMISSION}
                return error
        
        #Delete device
        result = self.database.delete_device({'device_name':parameter['device_name']})
        return result

    #Get a filtered device list if in the request evrything is fine
    #parameter -> parameter to filter the device list, type = dict
    #reqeust -> The columns you wish to get, type = list
    def get_device(self,chat_id, parameter, request):
        #Check if parameters are valid
        requiered_parameter = []
        optional_parameter = ['device_name','device_typ','device_location','home_name']
        parameter = self.check_parameter(parameter, requiered_parameter, optional_parameter)
        if parameter is None:
            error = {'status':ERROR_PARAMETER_NOT_VALID}
            return error
        request_allowed = ['device_name','device_location','device_typ','device_owner','device_friends','home_name','home_ower','chat_id','gateway_ip']
        if not self.check_request(request, request_allowed):
            error = {'status':ERROR_PARAMETER_NOT_VALID}
            return error

        #Create a independent copy for the second search
        parameter2 = deepcopy(parameter)

        #Search for devices in which the user is owner
        parameter['chat_id'] = chat_id
        result = self.database.get_from_device_table(parameter,request)
        if result['status'] is not OK:
            return result
        
        #Search for devices in which the user is friend
        #First find the user_name of the chat_id
        user = self.database.get_from_user_table({'chat_id':chat_id},['user_name'])
        if user['status'] is not OK:
            return user
        parameter2['device_friends'] = user['result'][0][0]
        result2 = self.database.get_from_device_table(parameter2, request)
        if result2['status'] is not OK:
            return result2

        #Return the results
        result['result2'] = result2['result']
        return result

    #Get all the homes in which the user owner or friend
    def get_homes(self,chat_id,parameter,request):
        #Check if parameters are valid
        requiered_parameter = []
        optional_parameter = ['home_name','gateway_ip']
        parameter = self.check_parameter(parameter, requiered_parameter, optional_parameter)
        if parameter is None:
            error = {'status':ERROR_PARAMETER_NOT_VALID}
            return error
        request_allowed = ['home_name','gateway_ip','home_owner','home_friends','chat_id']
        if not self.check_request(request, request_allowed):
            error = {'status':ERROR_PARAMETER_NOT_VALID}
            return error
        
        #Create a independent copy for the second search
        parameter2 = deepcopy(parameter)

        #Get the homes in which the user is owner
        parameter['chat_id'] = chat_id
        result = self.database.get_from_home_table(parameter,request)
        if result['status'] is not OK:
            return result

        #Get the homes in which the user friend
        #First find user_name of chat_id
        user = self.database.get_from_user_table({'chat_id':chat_id},['user_name'])
        parameter2['home_friends']= user['result'][0][0]
        result2 = self.database.get_from_home_table(parameter2,request)
        if result2['status'] is not OK:
            return result2

        #Return both lists
        result['result2'] = result2['result']
        return result
        
    #Get all users of a home if the request is fine
    def get_user(self,chat_id,parameter):
        #Check if parameters are valid
        requiered_parameter = ['home_name']
        optional_parameter = []
        parameter = self.check_parameter(parameter, requiered_parameter, optional_parameter)
        if parameter is None:
            error = {'status':ERROR_PARAMETER_NOT_VALID}
            return error
        
        #Check if a home with the name exist
        result = self.database.get_from_home_table({'home_name':parameter['home_name']},['home_owner', 'home_friends'])
        if result['status'] is not OK:
            return result
        if len(result['result'][0][0]) == 0:
            error = {'status':ERROR_HOME_NOT_EXIST}
            return error
        
        #Check if the user is authorized
        user = self.database.get_from_user_table({'chat_id':chat_id},['user_name','rights'])
        if user['status'] is not OK:
            return user
        if not(user['result'][0][0] == result['result'][0][0]):
            #Check if the user is admin
            if not(user['result'][0][1] == 'admin'):
                error = {'status':ERROR_NO_PERMISSION}
                return error
        
        #Return the owner and friend list
        return result

    #Add friend to the home if the request is fine
    def add_friend_home(self,chat_id, parameter):
        #Check if parameters are valid
        requiered_parameter = ['home_name','home_friends']
        optional_parameter = []
        parameter = self.check_parameter(parameter, requiered_parameter, optional_parameter)
        if parameter is None:
            error = {'status':ERROR_PARAMETER_NOT_VALID}
            return error
        
        #Check if the home and the friend exist or the friend is already added
        result = self.database.get_from_home_table({'home_name':parameter['home_name']},['chat_id','home_friends'])
        if result['status'] is not OK:
            return result
        if len(result['result']) == 0:
            error = {'status':ERROR_HOME_NOT_EXIST}
            return error
        if result['result'][0][1] is not None:
            if (parameter['home_friends'] in result['result'][0][1]):
                error = {'status':ERROR_FRIEND_ALREADY_ADDED}
                return error
        friend = self.database.exist_user({'user_name':parameter['home_friends']})
        if friend['status'] is not OK:
            return friend
        if friend['result'] == 'False':
            error = {'status':ERROR_FRIEND_NOT_EXIST}
        
        #Check if the user is allowed to add a friend
        admin = self.database.get_from_user_table({'chat_id':chat_id},['rights'])
        if result['status'] is not OK:
            return admin
        if admin['result'][0][0] is not 'admin':
            if not(result['result'][0][0] == chat_id):
                error = {'status':ERROR_NO_PERMISSION}
                return error
        
        #Add a friend to the home
        result = self.database.add_friend_home(parameter)
        if result['status'] is not OK:
            return result

        return result

    #Delete a friend from a home if the request is fine
    def delete_friend_home(self,chat_id, parameter):
        #Check if parameters are valid
        requiered_parameter = ['home_name','home_friends']
        optional_parameter = []
        parameter = self.check_parameter(parameter, requiered_parameter, optional_parameter)
        if parameter is None:
            error = {'status':ERROR_PARAMETER_NOT_VALID}
            return error

        #Check if the home exist
        result = self.database.get_from_home_table({'home_name':parameter['home_name']},['chat_id', 'home_friends'])
        if result['status'] is not OK:
            return result
        if len(result['result']) == 0:
            error = {'status':ERROR_HOME_NOT_EXIST}
            return error
        if result['result'][0][1] is None:
            error = {'status':ERROR_FRIEND_NOT_ADDED}
            return error
        if not parameter['home_friends'] in result['result'][0][1]:
            error = {'status':ERROR_FRIEND_NOT_ADDED}
            return error

        #Check if the user is allowed to delete a friend
        admin = self.database.get_from_user_table({'chat_id':chat_id},['rights'])
        if result['status'] is not OK:
            return admin
        if admin['result'][0][0] is not 'admin':
            if not(result['result'][0][0] == chat_id):
                error = {'status':ERROR_NO_PERMISSION}
                return error
        
        #Delete a friend to the home
        result = self.database.delete_friend_home(parameter)
        if result['status'] is not OK:
            return result

        return result

    #Add a friend to a device if the request is right
    def add_friend_device(self,chat_id,parameter):
        #Check if parameters are valid
        requiered_parameter = ['device_name','device_friends']
        optional_parameter = []
        parameter = self.check_parameter(parameter, requiered_parameter, optional_parameter)
        if parameter is None:
            error = {'status':ERROR_PARAMETER_NOT_VALID}
            return error

        #Check if the device exist
        result = self.database.get_from_device_table({'device_name':parameter['device_name']},['chat_id','device_friends'])
        if result['status'] is not OK:
            return result
        if len(result['result']) == 0:
            error = {'status':ERROR_NOT_EXIST}
            return error
        if result['result'][0][1] is not None:
            if (parameter['device_friends'] in result['result'][0][1]):
                error = {'status':ERROR_FRIEND_ALREADY_ADDED}
                return error
        friend = self.database.exist_user({'user_name':parameter['device_friends']})
        if friend['status'] is not OK:
            return friend
        if friend['result'] == 'False':
            error = {'status':ERROR_FRIEND_NOT_EXIST}

        #Check if the user is allowed to add a friend
        admin = self.database.get_from_user_table({'chat_id':chat_id},['rights'])
        if result['status'] is not OK:
            return admin
        if admin['result'][0][0] is not 'admin':
            if not(result['result'][0][0] == chat_id):
                error = {'status':ERROR_NO_PERMISSION}
                return error
        
        #Add a friend to the device
        result = self.database.add_friend_device(parameter)
        if result['status'] is not OK:
            return result

        return result

    #Delete a friend from a device if the reqeust is fine
    def delete_friend_device(self,chat_id,parameter):
        #Check if parameters are valid
        requiered_parameter = ['device_name','device_friends']
        optional_parameter = []
        parameter = self.check_parameter(parameter, requiered_parameter, optional_parameter)
        if parameter is None:
            error = {'status':ERROR_PARAMETER_NOT_VALID}
            return error

        #Check if the device exist
        result = self.database.get_from_device_table({'device_name':parameter['device_name']},['chat_id','device_friends'])
        if result['status'] is not OK:
            return result
        if len(result['result']) == 0:
            error = {'status':ERROR_NOT_EXIST}
            return error
        if result['result'][0][1] is None:
            error = {'status':ERROR_FRIEND_NOT_ADDED}
            return error
        if not parameter['device_friends'] in result['result'][0][1]:
            error = {'status':ERROR_FRIEND_NOT_ADDED}
            return error

        #Check if the user is allowed to add a friend
        admin = self.database.get_from_user_table({'chat_id':chat_id},['rights'])
        if result['status'] is not OK:
            return admin
        if admin['result'][0][0] is not 'admin':
            if not(result['result'][0][0] == chat_id):
                error = {'status':ERROR_NO_PERMISSION}
                return error
        
        #Add a friend to the device
        result = self.database.delete_friend_device(parameter)
        if result['status'] is not OK:
            return result

        return result

    #Check if the parameter are all valid
    def check_parameter(self, parameter, requiered_parameter, optional_parameter):
        valid ={}
        for req in requiered_parameter:
            if req in parameter:
                if len(parameter[req].encode('utf-8')) < 63:
                    valid[req] = parameter[req]
                else:
                    return None
            else:
                return None
        for opt in optional_parameter:
            if opt in parameter:
                if len(parameter[opt].encode('utf-8')) < 63:
                    valid[opt] = parameter[opt]
        
        return valid

    #Check the request list
    def check_request(self, request, allowed):
        valid = []
        for req in request:
            if req in allowed:
                valid.append(req)
        return valid
