from page_objects import init_page_objects


class TestSearchProduct:

    def test_search_with_keyword_dress(self, driver):
        init_page_objects(driver)
        home_page = driver.home_page_object
        driver.get(home_page.url)

        search_result = home_page.search_with_keyword('洋裝')
        titles = search_result.get_present_product_elements()
        for title_elem in titles:
            assert '洋裝' in title_elem.text, '"洋裝" is not included in the title.'

    def test_search_without_keyword(self, driver, products_info):
        init_page_objects(driver)
        home_page = driver.home_page_object
        driver.get(home_page.url)

        search_result = home_page.search_with_keyword('')
        num_all_products = products_info.shape[0]  # The first number in shape stands for the number of rows in the dataFrame
        product_elems = search_result.get_present_product_elements(num_all_products)

        for elem in product_elems:
            assert elem.text in products_info['title'].values, f'The product {elem.text} should not be displayed.'

    def test_search_with_keyword_hello(self, driver):
        init_page_objects(driver)
        home_page = driver.home_page_object
        driver.get(home_page.url)

        search_result = home_page.search_with_keyword('Hello')
        product_elems = search_result.get_present_product_elements()
        assert len(product_elems) == 0, f'There should not be any product in search result, but got {len(product_elems)}.'
