# database-api
The task of the database-api is to manage the database entries of the Smart Home Chatbot. It include the validation of parameters, the authorization and the execution.

##Interface
The database_api get interfaced by AMQP. With different queues you are able to call the following commands.
* exist_user
* add_user
* delete_user
* add_home
* delete_home
* add_device
* delete_device
* get_device
* get_homes
* get_users

### exist_user
This command allows you to check if a user already exist in the database.

Required json Payload:
````
"{'chat_id':'123456','parameter':{}}"
````

Optional a parameter user_name can be added then the user_name get checked.

Json result:

    "{'status':'ok','result':'True'}"


### add_user
This command allows you to add a new user to the database.

Required json Payload:

    "{'chat_id':'123456','parameter:{'user_name':'my_user_name'}'}"

Json result:

    "{'status':'ok'}"

### delete_user
This command allow you to delete a user from the database.

Required json Payload:

    "{'chat_id':'123456','parameter':{}"

If you are admin and you want to delete another user add the `user_name` to the parameter.

Json result:

    "{'status':'ok'}"

### add_home
This command allows you to add a home to the database.

Required json Payload:

    "{'chat_id':'12345','parameter':{'home_name':'my_home','gateway_ip':'1234'}}"

Json result:

  "{'status':'ok'}"

### delete_home
This command allows you to delete a command.

Required json Payload:

    "{'chat_id':'123456','parameter':{'home_name':'my_home'}}"

Json result:

    "{'status':'ok'}"

### add_device
This command allows you to add a new device to the database.

Required json Payload:

    "{'chat_id':'123456','parameter':{'device_name':'my_device','device_typ':'LED','device_location':'room','home_name':'my_home'}}"

Json result:

    "{'status':'ok'}"

### delete_device
This command allows you to delete a device from the database.

Required json Payload:

    "{'chat_id':'123456','parameter':{'device_name':'my_device'}}"

Json result:

    "{'status':'ok'}"

### get_device
This command allows you to search for devices in the database.

Required json Payload:

    "{'chat_id':'123456','parameter':{search_parameter},'request':[request_items]}"

possible search_parameter:
* device_name
* device_typ
* device_location
* device_owner
* home_name

possible request_items:
* device_name
* device_typ
* device_location
* home_name
* device_friends
* home_owner
* chat_id
* device_owner

Json result:

    "{'status':'ok','result':[[row1],[row2],..],'result2':[[row1],[row2],..]}"

result will be the devices in which you are device_owner and result2 will be the devices in which you are a friend.

### get_homes
This command allows you to get data of the home_table.

Required json Payload:
    "{'chat_id':'123456','parameter':{search_parameter},'request':[request_items]}"

possible search_parameter:
* home_name
* gateway_ip
* home_owner

possible request_items:
* home_name
* gateway_ip
* home_owner
* chat_id
* home_friends

Json result:
    "{'status':'ok','result':[[row1],[row2],..],'result2':[[row1],[row2],..]}"

result will be the homes in which you are home_owner and result2 will be the homes in which you are a friend.

<!-- ### get_users
This command allows you to get all the users of a home.

Required json Payload:

    "{'chat_id':'123456','parameter':{'home_name':'my_home'}}"

Json result:

    "{'status':'ok','result':[[home_owner, [home_friends]]]}" -->
