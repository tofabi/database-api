# database-api
The task of the database-api is to manage the database entries of the Smart Home Chatbot. It include the validation of parameters, the authorization and the execution.

## Interface
The database_api get interfaced by AMQP. Therefore a exchange with the name "db_exchange" was created, which can handle the following routing keys:
* user.add
* user.delete
* user.exist
* home.add
* home.delete
* home.get
* home.add_friend
* home.delete_friend
* device.add
* device.delete
* device.get
* device.add_friend
* device.delete_friend

### user.add
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

### user.exist
This command allows you to check if a user already exist in the database.

Required json Payload:
````
"{'chat_id':'123456','parameter':{}}"
````

Optional a parameter `user_name` can be added then the user_name get checked.

Json result:

    "{'status':'ok','result':'True'}"

### home.add
This command allows you to add a home to the database.

Required json Payload:

    "{'chat_id':'12345','parameter':{'home_name':'my_home','gateway_ip':'1234'}}"

Json result:

  "{'status':'ok'}"

### home.delete
This command allows you to delete a home.

Required json Payload:

    "{'chat_id':'123456','parameter':{'home_name':'my_home'}}"

Json result:

    "{'status':'ok'}"

### home.get
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

### home.add_friend
This command allows you to add a friend to a home.

Required json Payload:

    "{'chat_id':'123456','parameter':{'home_name':'my_home', 'home_friends':'myfriend'}}"

Json result:

    "{'status':'ok'}"

### home.delete_friend
This command allows you to delete a friend from a home.

Required json Payload:

    "{'chat_id':'123456','parameter':{'home_name':'my_home', 'home_friends':'myfriend'}}"

Json result:

    "{'status':'ok'}"

### device.add
This command allows you to add a new device to the database.

Required json Payload:

    "{'chat_id':'123456','parameter':{'device_name':'my_device','device_typ':'LED','device_location':'room','home_name':'my_home'}}"

Json result:

    "{'status':'ok'}"

### device.delete
This command allows you to delete a device from the database.

Required json Payload:

    "{'chat_id':'123456','parameter':{'device_name':'my_device'}}"

Json result:

    "{'status':'ok'}"

### device.get
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

### device.add_friend
This command allows you to add a friend to a device.

Required json Payload:

    "{'chat_id':'123456','parameter':{'device_name':'my_device', 'device_friends':'myfriend'}}"

Json result:

    "{'status':'ok'}"

### device.delete_friend
This command allows you to delete a friend from a device.

Required json Payload:

    "{'chat_id':'123456','parameter':{'device_name':'my_device', 'device_friends':'myfriend'}}"

Json result:

    "{'status':'ok'}"
