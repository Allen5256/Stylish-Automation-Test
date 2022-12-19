from api_objects import APIUtils
from test_data import domain


class GetProductsByCategoryAPI(APIUtils):
    def __init__(self, session, category='all'):
        super().__init__(session)
        self.url = f'{domain}api/1.0/products/{category}'

    def send_request(self):
        self.get_request()
        return self

    def get_product_list(self):
        return self.response.json().get('data')
