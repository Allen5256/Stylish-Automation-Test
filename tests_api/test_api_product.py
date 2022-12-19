import pytest

from api_objects import init_api_objects


class TestGetProductsByCategoryAPI:

    categories = [
        'men',
        'women',
        'accessories'
    ]

    @pytest.mark.parametrize('category', categories)
    def test_get_products_by_category_success(self, session, category):
        init_api_objects(session, category=category)
        api_obj = session.get_products_by_category_api_object

        # Verify all products show belong to the target category
        paging = 0
        while True:
            session.params = {'paging': paging}
            api_obj.send_request()
            response_code = api_obj.get_http_response_code()
            product_list = api_obj.get_product_list()

            assert response_code == 200, \
                f'The response code is supposed to be 200, but actually get {response_code}.'

            if len(product_list) == 0:
                break
            else:
                for product_info in product_list:
                    product_id = product_info['id']
                    product_category = product_info['category']
                    assert product_category == category, \
                        f'Target category: "{category}", the product(id: {product_id}) belongs to {product_category}.'

            paging += 1

    def test_get_products_by_category_failure(self, session):
        init_api_objects(session, category='invalid')
        api_obj = session.get_products_by_category_api_object

        # Send request with invalid category
        api_obj.send_request()
        response_code = api_obj.get_http_response_code()
        response_err_msg = api_obj.get_response_error_msg()

        assert response_code == 400, \
            f'The response code is supposed to be 200, but actually get {response_code}.'
        assert response_err_msg == 'Invalid Category', \
            f'The response error message is supposed to be "Invalid Category", but actually get {response_err_msg}.'


class TestGetProductsBySearch:
    def test_get_products_by_search_with_existing_keyword(self, session):
        init_api_objects(session)
        api_obj = session.get_products_by_search_api_object

        # Verify all products show have title including the keyword
        paging = 0
        while True:
            session.params = {
                'keyword': '洋裝',
                'paging': paging
            }
            api_obj.send_request()
            response_code = api_obj.get_http_response_code()
            product_list = api_obj.get_product_list()

            assert response_code == 200, \
                f'The response code is supposed to be 200, but actually get {response_code}.'

            if len(product_list) == 0:
                break
            else:
                for product_info in product_list:
                    product_title = product_info['title']
                    assert '洋裝' in product_title, \
                        f'the product title "{product_title}" contains no keyword: "洋裝".'

            paging += 1

    def test_get_products_by_search_with_non_existing_keyword(self, session):
        init_api_objects(session)
        api_obj = session.get_products_by_search_api_object

        paging = 0
        session.params = {
            'keyword': 'All',
            'paging': paging
        }
        api_obj.send_request()

        response_code = api_obj.get_http_response_code()
        product_list = api_obj.get_product_list()

        # Verify no product show in the response
        assert response_code == 200, \
            f'The response code is supposed to be 200, but actually get {response_code}.'

        assert len(product_list) == 0, \
            f'There should not be any product show, but actually get product list: {product_list}.'

    def test_get_products_by_search_without_keyword(self, session):
        init_api_objects(session)
        api_obj = session.get_products_by_search_api_object

        paging = 0
        session.params = {
            'paging': paging
        }
        api_obj.send_request()

        response_code = api_obj.get_http_response_code()
        response_err_msg = api_obj.get_response_error_msg()

        assert response_code == 400, \
            f'The response code is supposed to be 400, but actually get {response_code}.'
        assert response_err_msg == 'Search Keyword is required.', \
            f'The response error message is supposed to be "Search Keyword is required.", but actually get {response_err_msg}.'


class TestGetProductDetailsById:
    def test_get_product_details_by_id_success(self, session, db):
        init_api_objects(session)
        api_obj = session.get_products_details_by_id_api_object

        session.params = {
            'id': 201807242216
        }
        api_obj.send_request()
        response_code = api_obj.get_http_response_code()
        product_details = api_obj.get_product_details()

        assert response_code == 200, \
            f'The response code is supposed to be 200, but actually get {response_code}.'

        # Get product info from database by the same id
        target_cols = ('*',)
        target_table = 'product'
        where_condition = 'id=201807242216'
        result_df = db.select_data_as_df(target_cols, target_table, where_condition=where_condition)

        # Verify product details in response are correct
        for index, row in result_df.iterrows():
            for col_name, exp_value in row.items():
                response_value = product_details[col_name]
                # Exclude column main_image
                if col_name != 'main_image':
                    assert response_value == exp_value, \
                        f'Verifying: "{col_name}", expected value is "{exp_value}", but actually get {response_value}.'

    def test_get_product_details_by_invalid_id(self, session):
        init_api_objects(session)
        api_obj = session.get_products_details_by_id_api_object

        session.params = {
            'id': 1234567890
        }
        api_obj.send_request()
        response_code = api_obj.get_http_response_code()
        response_err_msg = api_obj.get_response_error_msg()

        assert response_code == 400, \
            f'The response code is supposed to be 400, but actually get {response_code}.'
        assert response_err_msg == 'Invalid Product ID', \
            f'The response error message is supposed to be "Invalid Product ID", but actually get {response_err_msg}.'
