from api_objects import APIUtils
from test_data import domain


class ProfileAPI(APIUtils):
    def __init__(self, session):
        super().__init__(session)
        self.url = f'{domain}api/1.0/user/profile'

    def send_request(self):
        self.get_request()
        return self

    def get_profile_data(self):
        return self.response.json().get('data')
