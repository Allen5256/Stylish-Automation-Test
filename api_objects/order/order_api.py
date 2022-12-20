import json

from api_objects import APIUtils
from test_data import domain


class OrderAPI(APIUtils):
    def __init__(self, session):
        super().__init__(session)
        self.url = f'{domain}api/1.0/order'
        self.payload = {
            'prime': '',
            'order': {
                'shipping': '',
                'payment': '',
                'subtotal': 0,
                'freight': 0,
                'total': 0,
                'recipient': {
                    'name': '',
                    'phone': '',
                    'email': '',
                    'address': '',
                    'time': ''
                },
                'list': []
            }
        }
        self.product_format = {
            'color': {
                'code': '',
                'name': ''
            },
            'id': '',
            'image': '',
            'name': '',
            'price': 0,
            'qty': 0,
            'size': ''
        }

    def send_request(self):
        self.post_request(json=self.payload)
        return self

    def prepare_order_information(self, test_data):
        order_info = {}
        recipient_info = {}
        product_info = {}

        processed_data = self.preprocess_payload_data(test_data)
        for key, value in processed_data.items():
            if key in ['shipping', 'payment', 'subtotal', 'freight', 'total']:
                order_info[key] = value
            if key in ['recipient_name', 'phone', 'email', 'address', 'time']:
                if key == 'recipient_name':
                    recipient_info['name'] = value
                else:
                    recipient_info[key] = value
            if key in ['color', 'id', 'image', 'product_name', 'price', 'qty', 'size']:
                if key == 'product_name':
                    product_info['name'] = value
                else:
                    product_info[key] = value

        return order_info, recipient_info, product_info

    def set_order_info_to_payload(self, order_info):
        for key, value in order_info.items():
            default_type = type(self.payload['order'][key])
            if isinstance(order_info[key], type(None)):
                pass
            else:
                order_info[key] = default_type(value)
        self.payload['order'].update(order_info)
        return self

    def set_recipient_info_to_order(self, recipient_info):
        for key, value in recipient_info.items():
            default_type = type(self.payload['order']['recipient'][key])
            if isinstance(recipient_info[key], type(None)):
                pass
            else:
                recipient_info[key] = default_type(value)
        self.payload['order']['recipient'].update(recipient_info)
        return self

    def set_product_to_order(self, product_info):
        for key, value in product_info.items():
            default_type = type(self.product_format[key])
            if isinstance(product_info[key], type(None)):
                pass
            elif default_type is dict:
                if type(value) is dict:
                    value = json.dumps(value)
                product_info[key] = json.loads(value)
            else:
                product_info[key] = default_type(value)
        self.payload['order']['list'].append(product_info)
        return self

    def get_order_number(self):
        return self.response.json().get('data').get('number')
