import pytest

from api_objects import init_api_objects
from test_data import login_info_0, get_row_data, preprocess_data_in_row

excel_name = 'Stylish-Test Case.xlsx'
create_product_success_sheet_name = 'API Create Product Success'
create_product_failed_sheet_name = 'API Create Product Failed'

default_test_data = {
    'category': 'women',
    'title': '連身裙',
    'description': '詳細內容',
    "price": '100',
    'texture': '棉質',
    'wash': '手洗',
    'place': 'Taiwan',
    'note': 'Notes',
    'color_ids': '1',
    'sizes': 'F',
    'story': 'Story Content',
    'main_image': 'sample image',
    'other_images_1': 'sample image',
    'other_images_2': 'sample image'
}


class TestCreateAndDeleteProductAPI:

    @pytest.mark.parametrize('row_data', get_row_data(excel_name, create_product_success_sheet_name))
    def test_api_create_and_delete_product_success(self, login_session, row_data):
        init_api_objects(login_session)
        create_product_api_object = login_session.create_product_api_object
        delete_product_api_object = login_session.delete_product_api_object
        get_products_details_by_id_api_object = login_session.get_products_details_by_id_api_object

        test_data = preprocess_data_in_row(row_data).to_dict()

        try:
            create_response_code = create_product_api_object\
                .set_form_data(**test_data)\
                .set_form_files(test_data)\
                .send_request()\
                .get_http_response_code()
            product_id = create_product_api_object.get_product_id()

            assert create_response_code == 200, \
                f'The response code is supposed to be 200, but actually get {create_response_code}.'
            assert product_id is not None, \
                'The response contains no product id, please check it out!'

            login_session.params = {
                'id': product_id
            }
            product_details = get_products_details_by_id_api_object\
                .send_request()\
                .get_product_details()

            for key, value in product_details.items():
                if key == 'id':
                    assert value == product_id
                elif key == 'main_image':
                    assert value == f'http://54.201.140.239/assets/{product_id}/mainImage.jpg'
                elif key == 'images':
                    num_other_images = len(create_product_api_object.files) - 1
                    assert len(value) == num_other_images
                elif key == 'variants':
                    # TODO 補上驗證
                    pass
                elif key == 'colors':
                    # TODO 補上驗證
                    pass
                elif key == 'sizes':
                    # TODO 補上驗證
                    pass
                else:
                    exp_value = create_product_api_object.form_data.get(key)
                    assert value == exp_value, \
                        f'Verifying {key}: Expect: "{exp_value}", but actually get "{value}".'
        finally:
            delete_response_code = delete_product_api_object\
                .set_product_id_to_url(product_id)\
                .send_request()\
                .get_http_response_code()

            assert delete_response_code == 200, \
                f'The response code is supposed to be 200, but actually get {delete_response_code}.'

    @pytest.mark.parametrize('row_data', get_row_data(excel_name, create_product_failed_sheet_name))
    def test_api_create_product_failed(self, login_session, row_data):
        init_api_objects(login_session)
        create_product_api_object = login_session.create_product_api_object
        delete_product_api_object = login_session.delete_product_api_object

        test_data = preprocess_data_in_row(row_data).to_dict()
        exp_err_msg = test_data.get('err_message')

        create_response_code = create_product_api_object\
            .set_form_data(**test_data)\
            .set_form_files(test_data)\
            .send_request()\
            .get_http_response_code()
        response_err_msg = create_product_api_object.get_response_error_msg()

        try:
            assert create_response_code == 400, \
                f'The response code is supposed to be 400, but actually get {create_response_code}.'
            assert response_err_msg == exp_err_msg, \
                f'The error message is supposed to be "{exp_err_msg}", but actually get "{response_err_msg}".'
        finally:
            product_id = create_product_api_object.get_product_id()
            if product_id is not None:
                delete_product_api_object\
                    .set_product_id_to_url(product_id)\
                    .send_request()

    def test_api_create_product_without_login(self, session):
        init_api_objects(session)
        create_product_api_object = session.create_product_api_object

        create_response_code = create_product_api_object\
            .set_form_data(**default_test_data)\
            .set_form_files(default_test_data)\
            .send_request()\
            .get_http_response_code()
        response_err_msg = create_product_api_object.get_response_error_msg()

        try:
            assert create_response_code == 401, \
                f'The response code is supposed to be 401, but actually get {create_response_code}.'
            assert response_err_msg == 'Unauthorized', \
                f'The error message is supposed to be "Unauthorized", but actually get "{response_err_msg}".'
        finally:
            login_api_object = session.login_api_object
            delete_product_api_object = session.delete_product_api_object

            login_info_0['provider'] = 'native'
            login_api_object\
                .set_payload_attribute(**login_info_0)\
                .send_request()

            product_id = create_product_api_object.get_product_id()
            if product_id is not None:
                delete_product_api_object\
                    .set_product_id_to_url(product_id)\
                    .send_request()

    def test_api_create_product_with_invalid_access_token(self, login_session):
        init_api_objects(login_session)
        logout_api_object = login_session.logout_api_object
        create_product_api_object = login_session.create_product_api_object

        logout_api_object.send_request()

        create_response_code = create_product_api_object\
            .set_form_data(**default_test_data)\
            .set_form_files(default_test_data)\
            .send_request()\
            .get_http_response_code()
        response_err_msg = create_product_api_object.get_response_error_msg()

        try:
            assert create_response_code == 403, \
                f'The response code is supposed to be 403, but actually get {create_response_code}.'
            assert response_err_msg == 'Invalid Access Token', \
                f'The error message is supposed to be "Invalid Access Token", but actually get "{response_err_msg}".'
        finally:
            login_api_object = login_session.login_api_object
            delete_product_api_object = login_session.delete_product_api_object

            login_info_0['provider'] = 'native'
            login_api_object\
                .set_payload_attribute(**login_info_0)\
                .send_request()

            product_id = create_product_api_object.get_product_id()
            if product_id is not None:
                delete_product_api_object\
                    .set_product_id_to_url(product_id)\
                    .send_request()

    def test_api_delete_product_without_login(self, session):
        init_api_objects(session)
        api_obj = session.delete_product_api_object

        response_code = api_obj.send_request().get_http_response_code()
        response_err_msg = api_obj.get_response_error_msg()

        assert response_code == 401, \
            f'The response code is supposed to be 401, but actually get {response_code}.'
        assert response_err_msg == 'Unauthorized', \
            f'The error message is supposed to be "Unauthorized", but actually get "{response_err_msg}".'

    def test_api_delete_product_with_invalid_access_token(self, login_session):
        init_api_objects(login_session)
        logout_api_object = login_session.logout_api_object
        delete_product_api_object = login_session.delete_product_api_object

        logout_api_object.send_request()

        response_code = delete_product_api_object\
            .send_request()\
            .get_http_response_code()
        response_err_msg = delete_product_api_object.get_response_error_msg()

        assert response_code == 403, \
            f'The response code is supposed to be 403, but actually get {response_code}.'
        assert response_err_msg == 'Invalid Access Token', \
            f'The error message is supposed to be "Invalid Access Token", but actually get "{response_err_msg}".'
