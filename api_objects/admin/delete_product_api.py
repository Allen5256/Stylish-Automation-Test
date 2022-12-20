from api_objects import APIUtils
from test_data import domain


class DeleteProductAPI(APIUtils):
    def __init__(self, session, product_id=0):
        super().__init__(session)
        self.url = f'{domain}api/1.0/admin/product/{product_id}'

    def send_request(self):
        self.delete_request()
        return self

    def set_product_id_to_url(self, product_id):
        self.url = f'{domain}api/1.0/admin/product/{product_id}'
        return self

    def get_product_id(self):
        return self.response.json().get('data').get('_product_id')
