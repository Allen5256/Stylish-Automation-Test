import pytest

from page_objects import init_page_objects


class TestCategory:
    categories = [
        'women',
        'men',
        'accessories'
    ]

    @pytest.mark.parametrize('category', categories)
    def test_category_with_correct_product(self, driver, category, products_info):
        init_page_objects(driver)
        home_page = driver.home_page_object
        driver.get(home_page.url)

        product_elems = home_page.click_category_btn(category).get_present_product_elements()
        target_products = products_info[products_info['category'] == category]['title']
        for elem in product_elems:
            assert elem.text in target_products.values, f'The product should not belong to {category} category.'
