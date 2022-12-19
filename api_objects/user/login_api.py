from api_objects import APIUtils
from test_data import domain


class LoginAPI(APIUtils):
    def __init__(self, session):
        super().__init__(session)
        self.url = f'{domain}api/1.0/user/login'
        self.payload = {
            'provider': '',
            'email': '',
            'password': ''
        }

    def send_request(self):
        self.post_request(json=self.payload)
        return self

    def get_access_token(self):
        return self.response.json()['data']['access_token']

    def get_user_info(self):
        return self.response.json()['data']['user']
