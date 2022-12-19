import pytest

from page_objects import init_page_objects
from test_data import *


class TestLoginPage:
    results = [
        'success',
        'failed'
    ]

    @pytest.mark.parametrize('result', results)
    def test_login_logout(self, driver, result, worker_id):
        init_page_objects(driver)
        login_page = driver.login_page_object
        driver.get(login_page.login_url)

        if result == 'success':
            profile_page = login_page.login(worker_id)
            alert = profile_page.get_alert()
            assert alert.text == 'Login Success', f'Login failed, check the alert message: {alert.text}'
            alert.accept()

            target_key = 'jwtToken'
            jwt_token = profile_page.get_local_storage_item(target_key)
            assert jwt_token is not None, f'The key does not exist in local storage: {target_key}'

            profile_page.logout()
            alert = profile_page.get_alert()
            assert alert.text == 'Logout Success', f'Logout failed, check the alert message: {alert.text}'
            alert.accept()

        elif result == 'failed':
            bad_login_info = {
                'email': 'iAmWrong@email.com',
                'password': 'iAmWrongPassword'
            }

            alert = login_page.login(worker_id, login_info=bad_login_info).get_alert()
            assert alert.text == 'Login Failed', 'Fatal error! Login should not succeed with wrong information!'
            alert.accept()

    def test_login_with_invalid_token(self, driver, worker_id):
        init_page_objects(driver)
        login_page = driver.login_page_object
        driver.get(login_page.login_url)

        profile_page = login_page.login(worker_id)
        alert = profile_page.get_alert()
        assert alert.text == 'Login Success', 'Login failed, check the alert message: {alert.text}'
        alert.accept()

        target_key = 'jwtToken'
        jwt_token = profile_page.get_local_storage_item(target_key)
        assert jwt_token is not None, 'The key does not exist in local storage: {target_key}'

        back_to_login_page = profile_page.logout()
        alert = back_to_login_page.get_alert()
        assert alert.text == 'Logout Success', f'Logout failed, check the alert message: {alert.text}'
        alert.accept()

        back_to_login_page.set_local_storage_item(target_key, jwt_token)
        alert = back_to_login_page.head_to_profile_page().get_alert()
        assert alert.text == 'Invalid Access Token', 'Something went wrong but not token error, check the alert message: {alert.text}'
        alert.accept()
