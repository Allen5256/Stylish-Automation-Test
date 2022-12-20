class APIUtils:
    def __init__(self, session):
        self.session = session
        self.payload = {}
        self.form_data = {}
        self.form_files = {}
        self.url = None
        self.response = None

    def set_payload_attribute(self, **kwargs):
        payload_body = self.payload.copy()
        for key, value in kwargs.items():
            # 只處理 payload 需要的欄位
            if key in payload_body:
                payload_body[key] = value
        self.payload = self.preprocess_payload_data(payload_body)
        return self

    def preprocess_payload_data(self, data):
        copy_data = data.copy()
        for key, value in copy_data.items():
            if value == 'None':
                data[key] = None
            elif value == '<remove attribute>':
                del data[key]
            else:
                data[key] = value
        return data

    def get_request(self, **kwargs):
        self._request('get', **kwargs)
        return self

    def post_request(self, **kwargs):
        self._request('post', **kwargs)
        return self

    def delete_request(self, **kwargs):
        self._request('delete', **kwargs)
        return self

    def put_request(self, **kwargs):
        self._request('put', **kwargs)
        return self

    def _request(self, verb, **kwargs):
        self.response = self.session.request(verb, self.url, **kwargs)

    def get_http_response_code(self):
        return self.response.status_code

    def get_response_error_msg(self):
        return self.response.json().get('errorMsg')
