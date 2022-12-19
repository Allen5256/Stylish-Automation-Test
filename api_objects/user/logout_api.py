from api_objects import APIUtils
from test_data import domain


class LogoutAPI(APIUtils):
    def __init__(self, session):
        super().__init__(session)
        self.url = f'{domain}api/1.0/user/logout'

    def send_request(self):
        self.post_request()
        return self
