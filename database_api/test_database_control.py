from .database_control import database_control

class TestCheckParameter:

    def test_correct_data(self):
        testClass = database_control('text','test')
        chat_id = '123'
        parameter = {'device_name':'device','home_name':'home'}
        required_parameter = ['device_name']
        optional_parameter = ['home_name','owner']

        assert testClass.check_parameter(chat_id, parameter, required_parameter, optional_parameter)

    def test_wrong_data(self):
        testClass = database_control('text','test')
        chat_id = '123'
        parameter = {'owner':'Iam','home_name':'home'}
        required_parameter = ['device_name']
        optional_parameter = ['home_name','owner']

        assert not testClass.check_parameter(chat_id, parameter, required_parameter, optional_parameter)

class TestCheckRequest:

    def test_correct_data(self):
        testClass = database_control('text','test')
        request = ['device_name','device_typ']
        allowed = ['device_name','device_typ','device_location']

        assert testClass.check_request(request,allowed)

    def test_wrong_data(self):
        testClass = database_control('text','test')
        request = ['device_name','device_owner']
        allowed = ['device_name','device_type','device_location']

        assert not testClass.check_request(request,allowed)