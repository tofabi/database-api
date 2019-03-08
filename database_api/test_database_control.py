from .database_control import database_control

class TestCheckParameter:

    def test_correct_data(self):
        testClass = database_control('text','test')
        parameter = {'device_name':'device','home_name':'home'}
        required_parameter = ['device_name']
        optional_parameter = ['home_name','owner']

        assert len(testClass.check_parameter(parameter, required_parameter, optional_parameter)) == len(parameter)

    def test_wrong_data(self):
        testClass = database_control('text','test')
        parameter = {'owner':'Iam','home_name':'home'}
        required_parameter = ['device_name']
        optional_parameter = ['home_name','owner']

        assert testClass.check_parameter(parameter, required_parameter, optional_parameter) is None

class TestCheckRequest:

    def test_correct_data(self):
        testClass = database_control('text','test')
        request = ['device_name','device_typ']
        allowed = ['device_name','device_typ','device_location']

        assert len(testClass.check_request(request,allowed)) == len(request)

    def test_wrong_data(self):
        testClass = database_control('text','test')
        request = ['device_name','device_owner']
        allowed = ['device_name','device_type','device_location']

        assert len(testClass.check_request(request,allowed)) == 1