from api_objects import APIUtils
from test_data import domain


class GetProductsBySearchAPI(APIUtils):
    def __init__(self, session):
        super().__init__(session)
        self.url = f'{domain}api/1.0/products/search'

    def send_request(self):
        self.get_request()
        return self

    def get_product_list(self):
        return self.response.json().get('data')
