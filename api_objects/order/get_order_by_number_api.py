from api_objects import APIUtils
from test_data import domain


class GetOrderByNumberAPI(APIUtils):
    def __init__(self, session, order_number=0):
        super().__init__(session)
        self.url = f'{domain}api/1.0/order/{order_number}'

    def send_request(self):
        self.get_request()
        return self

    def set_order_number_to_url(self, order_number):
        self.url = f'{domain}api/1.0/order/{order_number}'
        return self

    def get_response_data(self):
        return self.response.json().get('data')

    def get_response_order_number(self):
        return self.response.json().get('data').get('number')

    def get_response_details(self):
        return self.response.json().get('data').get('details')
