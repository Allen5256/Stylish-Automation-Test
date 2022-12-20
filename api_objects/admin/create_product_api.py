from api_objects import APIUtils
from test_data import domain


class CreateProductAPI(APIUtils):
    def __init__(self, session):
        super().__init__(session)
        self.url = f'{domain}api/1.0/admin/product'
        self.form_data = {
            'category': '',
            'title': '',
            'description': '',
            "price": 0,
            'texture': '',
            'wash': '',
            'place': '',
            'note': '',
            'color_ids': [],
            'sizes': [],
            'story': ''
        }
        self.files = []

    def send_request(self):
        self.post_request(data=self.form_data, files=self.files)
        return self

    def set_form_data(self, **kwargs):
        form_data_body = self.form_data.copy()
        for key, value in kwargs.items():
            # 只處理 form_data 需要的欄位
            if key in form_data_body:
                default_type = type(self.form_data[key])
                if default_type is list and value is not None and value != '':
                    value_list = value.split(',')
                    for i in range(len(value_list)):
                        if value_list[i].isdigit():
                            value_list[i] = int(value_list[i])
                    form_data_body[key] = value_list
                elif key == 'price':
                    if value in ['', 'text']:
                        form_data_body[key] = value
                    else:
                        form_data_body[key] = int(value)
                else:
                    form_data_body[key] = default_type(value)
        self.form_data = self.preprocess_payload_data(form_data_body)
        return self

    def set_form_files(self, test_data):
        self.preprocess_payload_data(test_data)
        for key, value in test_data.items():
            if value == 'sample image':
                if key == 'main_image':
                    self.files.append(('main_image', open(r'test_data/product_images/mainImage.jpg', 'rb')))
                if key == 'other_images_1':
                    self.files.append(('other_images', open(r'test_data/product_images/otherImage0.jpg', 'rb')))
                if key == 'other_images_2':
                    self.files.append(('other_images', open(r'test_data/product_images/otherImage1.jpg', 'rb')))
        return self

    def get_product_id(self):
        product_id = None
        response_data = self.response.json().get('data')
        if response_data is not None:
            product_id = response_data.get('product_id')
        return product_id
