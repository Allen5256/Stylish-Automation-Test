import json

import pytest

from api_objects import init_api_objects
from test_data import get_row_data

excel_name = 'Stylish-Test Case.xlsx'
order_failed_sheet_name = 'API Order Failed'

default_order_info = {
    'shipping': 'delivery',
    'payment': 'credit_card',
    'subtotal': 2399,
    'freight': 30,
    'total': 2429
}
default_product_info = {
    'color': '{"code":"FFFFFF","name":"白色"}',
    'id': '201807242216',
    'image': 'http://54.201.140.239/assets/201807242216/main.jpg',
    'name': '時尚輕鬆休閒西裝',
    'price': 2399,
    'qty': 1,
    'size': 'M'
}
default_recipient_info = {
    'name': 'Allen Lee',
    'phone': '0987654321',
    'email': 'allenlee@email.com',
    'address': '八德路123',
    'time': 'anytime'
}


class TestOrderAPI:

    def test_order_success(self, login_session, prime):
        init_api_objects(login_session)
        order_api_object = login_session.order_api_object

        order_api_object.set_payload_attribute(prime=prime)
        order_api_object.set_order_info_to_payload(default_order_info)\
            .set_recipient_info_to_order(default_recipient_info)\
            .set_product_to_order(default_product_info)

        response_code = order_api_object.send_request().get_http_response_code()
        response_order_number = order_api_object.get_order_number()
        assert response_code == 200, \
            f'The response code is supposed to be 200, but actually get {response_code}.'
        assert response_order_number is not None, \
            'The response contains no order number, please check it out!'

    @pytest.mark.parametrize('test_data', get_row_data(excel_name, order_failed_sheet_name))
    def test_order_failed(self, login_session, test_data):
        init_api_objects(login_session)
        order_api_object = login_session.order_api_object

        data_dict = test_data.to_dict()
        prime = data_dict.get('prime')
        order_info, recipient_info, product_info = \
            order_api_object.prepare_order_information(data_dict)

        order_api_object.set_payload_attribute(prime=prime)
        order_api_object.set_order_info_to_payload(order_info)\
            .set_recipient_info_to_order(recipient_info)\
            .set_product_to_order(product_info)

        response_code = order_api_object.send_request().get_http_response_code()
        response_err_msg = order_api_object.get_response_error_msg()

        exp_code = int(data_dict.get('code'))
        exp_err_msg = data_dict.get('err_message')
        assert response_code == exp_code, \
            f'The response code is supposed to be {exp_code}, but actually get {response_code}.'
        assert response_err_msg == exp_err_msg, \
            f'The error message responded is supposed to be "{exp_err_msg}", but actually get "{response_err_msg}".'

    def test_order_without_login(self, session, prime):
        init_api_objects(session)
        order_api_object = session.order_api_object

        order_api_object.set_payload_attribute(prime=prime)
        order_api_object.set_order_info_to_payload(default_order_info)\
            .set_recipient_info_to_order(default_recipient_info)\
            .set_product_to_order(default_product_info)

        response_code = order_api_object.send_request().get_http_response_code()
        response_err_msg = order_api_object.get_response_error_msg()

        assert response_code == 401, \
            f'The response code is supposed to be 401, but actually get {response_code}.'
        assert response_err_msg == 'Unauthorized', \
            f'The error message responded is supposed to be "Unauthorized", but actually get "{response_err_msg}".'

    def test_order_with_invalid_access_token(self, login_session, prime):
        init_api_objects(login_session)
        logout_api_object = login_session.logout_api_object
        order_api_object = login_session.order_api_object

        logout_api_object.send_request()

        order_api_object.set_payload_attribute(prime=prime)
        order_api_object.set_order_info_to_payload(default_order_info)\
            .set_recipient_info_to_order(default_recipient_info)\
            .set_product_to_order(default_product_info)

        response_code = order_api_object.send_request().get_http_response_code()
        response_err_msg = order_api_object.get_response_error_msg()

        assert response_code == 403, \
            f'The response code is supposed to be 403, but actually get {response_code}.'
        assert response_err_msg == 'Invalid Access Token', \
            f'The error message responded is supposed to be "Invalid Access Token", but actually get "{response_err_msg}".'


class TestGetOrderByNumber:

    def test_get_order_by_number_success(self, login_session, db):
        init_api_objects(login_session)
        get_order_by_number_api_object = login_session.get_order_by_number_api_object

        order_number = 1116703646060
        response_code = get_order_by_number_api_object\
            .set_order_number_to_url(order_number)\
            .send_request()\
            .get_http_response_code()

        assert response_code == 200, \
            f'The response code is supposed to be 200, but actually get {response_code}.'

        response_data = get_order_by_number_api_object.get_response_data()

        target_cols = ('*',)
        target_table = 'order_table'
        where_condition = f'number={order_number}'
        result_df = db.select_data_as_df(
            target_cols,
            target_table,
            where_condition=where_condition
        )

        for index, row in result_df.iterrows():
            exp_data = row.to_dict()
            exp_data['details'] = json.loads(exp_data['details'])
            assert response_data == exp_data

    def test_get_order_by_non_existing_number(self, login_session):
        init_api_objects(login_session)
        get_order_by_number_api_object = login_session.get_order_by_number_api_object

        response_code = get_order_by_number_api_object\
            .set_order_number_to_url(123)\
            .send_request()\
            .get_http_response_code()
        response_err_msg = get_order_by_number_api_object.get_response_error_msg()

        assert response_code == 400, \
            f'The response code is supposed to be 400, but actually get {response_code}.'
        assert response_err_msg == 'Order Not Found.',\
            f'The error message responded is supposed to be "Order Not Found.", but actually get "{response_err_msg}".'

    def test_get_order_by_number_without_login(self, session):
        init_api_objects(session)
        get_order_by_number_api_object = session.get_order_by_number_api_object

        order_number = 1116703646060
        response_code = get_order_by_number_api_object\
            .set_order_number_to_url(order_number)\
            .send_request()\
            .get_http_response_code()
        response_err_msg = get_order_by_number_api_object.get_response_error_msg()

        assert response_code == 401, \
            f'The response code is supposed to be 401, but actually get {response_code}.'
        assert response_err_msg == 'Unauthorized',\
            f'The error message responded is supposed to be "Unauthorized", but actually get "{response_err_msg}".'

    def test_get_order_by_number_with_invalid_access_token(self, login_session):
        init_api_objects(login_session)
        logout_api_object = login_session.logout_api_object
        get_order_by_number_api_object = login_session.get_order_by_number_api_object

        logout_api_object.send_request()

        order_number = 1116703646060
        response_code = get_order_by_number_api_object\
            .set_order_number_to_url(order_number)\
            .send_request()\
            .get_http_response_code()
        response_err_msg = get_order_by_number_api_object.get_response_error_msg()

        assert response_code == 403, \
            f'The response code is supposed to be 403, but actually get {response_code}.'
        assert response_err_msg == 'Invalid Access Token',\
            f'The error message responded is supposed to be "Invalid Access Token", but actually get "{response_err_msg}".'
