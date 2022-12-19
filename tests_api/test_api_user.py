import pytest

from api_objects import init_api_objects
from test_data import login_info_0, get_row_data

excel_name = 'Stylish-Test Case.xlsx'
login_failed_sheet_name = 'API Login Failed'


class TestLoginAPI:
    def test_login_success(self, session, db):
        init_api_objects(session)
        login_api_object = session.login_api_object

        # Set payload attribute and login
        login_info_0['provider'] = 'native'
        login_api_object.set_payload_attribute(**login_info_0)
        response_code = login_api_object.send_request().get_http_response_code()

        assert response_code == 200, \
            f'The response code is supposed to be 200, but actually get {response_code}.'

        # Get response data
        response_token = login_api_object.get_access_token()
        response_user = login_api_object.get_user_info()

        # Get relevant data by email from database
        login_email = login_info_0.get('email')
        target_cols = ('id', 'provider', 'name', 'email', 'access_token')
        target_table = 'user'
        where_condition = f'email="{login_email}"'
        result_df = db.select_data_as_df(target_cols, target_table, where_condition=where_condition)

        for index, row in result_df.iterrows():
            for col_name, exp_value in row.items():
                if col_name == 'access_token':
                    assert response_token == exp_value, 'Fatal: Token wrong! The login should not succeed!'
                else:
                    response_value = response_user.get(col_name)
                    assert response_value == exp_value, \
                        f'Verifying attribute: "{col_name}", expected value is "{exp_value}", but get {response_value}.'

    @pytest.mark.parametrize('test_data', get_row_data(excel_name, login_failed_sheet_name))
    def test_login_failed(self, session, test_data):
        init_api_objects(session)
        login_api_object = session.login_api_object

        # Set payload attribute
        data_dict = test_data.to_dict()
        login_api_object.set_payload_attribute(**data_dict)

        # Login
        response_code = login_api_object.send_request().get_http_response_code()
        response_err_msg = login_api_object.get_response_error_msg()

        exp_status_code = int(data_dict.get('status_code'))
        exp_err_msg = data_dict.get('err_message')
        assert response_code == exp_status_code, \
            f'The response code is supposed to be {exp_status_code}, but actually get "{response_code}".'
        assert response_err_msg == exp_err_msg, \
            f'The error message responded is supposed to be "{exp_err_msg}", but actually get "{response_err_msg}".'


class TestLogoutAPI:
    def test_logout_success(self, login_session):
        init_api_objects(login_session)
        logout_api_object = login_session.logout_api_object

        # Logout
        response_code = logout_api_object.send_request().get_http_response_code()

        assert response_code == 200, \
            f'The response code is supposed to be 200, but actually get {response_code}.'

    def test_logout_with_invalid_token(self, login_session):
        init_api_objects(login_session)
        logout_api_object = login_session.logout_api_object

        # Logout -> access token invalid
        logout_api_object.send_request()
        # Logout again
        response_code = logout_api_object.send_request().get_http_response_code()
        response_err_msg = logout_api_object.get_response_error_msg()

        assert response_code == 403, \
            f'The response code is supposed to be 403, but actually get {response_code}.'
        assert response_err_msg == 'Invalid Access Token', \
            f'The response error message is supposed to be "Invalid Access Token", but actually get {response_err_msg}.'

    def test_logout_without_token(self, session):
        init_api_objects(session)
        login_api_object = session.login_api_object
        logout_api_object = session.logout_api_object

        # Login first
        login_api_object.send_request()

        # Logout directly without access token
        response_code = logout_api_object.send_request().get_http_response_code()
        response_err_msg = logout_api_object.get_response_error_msg()

        assert response_code == 401, \
            f'The response code is supposed to be 401, but actually get {response_code}.'
        assert response_err_msg == 'Unauthorized', \
            f'The response code is supposed to be "Unauthorized", but actually get {response_err_msg}.'


class TestProfileAPI:
    def test_get_profile_success(self, login_session, db):
        init_api_objects(login_session)
        profile_api_object = login_session.profile_api_object

        # Login to get access token first
        access_token = login_session.headers.get('Authorization')

        # Get user profile info
        response_code = profile_api_object.send_request().get_http_response_code()
        response_profile_data = profile_api_object.get_profile_data()

        # Get relevant data by access token from database
        target_cols = ('id', 'provider', 'name', 'email')
        target_table = 'user'
        where_condition = f'access_token="{access_token}"'
        result_df = db.select_data_as_df(target_cols, target_table, where_condition=where_condition, index_col='id')

        assert response_code == 200, \
            f'The response code is supposed to be 200, but actually get {response_code}.'

        for index, row in result_df.iterrows():
            for col_name, exp_value in row.items():
                response_value = response_profile_data.get(col_name)
                assert response_value == exp_value, \
                    f'Verifying attribute: "{col_name}", expected value is "{exp_value}", but get {response_value}.'

    def test_get_profile_with_invalid_token(self, login_session):
        init_api_objects(login_session)
        logout_api_object = login_session.logout_api_object
        profile_api_object = login_session.profile_api_object

        # Logout -> access token invalid
        logout_api_object.send_request()
        # Get profile
        response_code = profile_api_object.send_request().get_http_response_code()
        response_err_msg = profile_api_object.get_response_error_msg()

        assert response_code == 403, \
            f'The response code is supposed to be 403, but actually get {response_code}.'
        assert response_err_msg == 'Invalid Access Token', \
            f'The response code is supposed to be "Invalid Access Token", but actually get {response_err_msg}.'

    def test_get_profile_without_token(self, session):
        init_api_objects(session)
        profile_api_object = session.profile_api_object

        # Get profile directly without access token
        response_code = profile_api_object.send_request().get_http_response_code()
        response_err_msg = profile_api_object.get_response_error_msg()

        assert response_code == 401, \
            f'The response code is supposed to be 401, but actually get {response_code}.'
        assert response_err_msg == 'Unauthorized', \
            f'The response code is supposed to be "Unauthorized", but actually get {response_err_msg}.'
