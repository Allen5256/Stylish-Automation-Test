from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from page_objects import CommonPage
from test_data import domain


class HomePage(CommonPage):
    def __init__(self, driver):
        super().__init__(driver)
        self.url = domain
        self.search_input_locator = (By.CSS_SELECTOR, 'input.header__search-input')
        self.product_titles_locator = (By.CSS_SELECTOR, 'div.product__title')

    def search_with_keyword(self, keyword):
        search_input_elem = self.find_clickable_element(self.search_input_locator)
        search_input_elem.send_keys(keyword)
        search_input_elem.send_keys(Keys.ENTER)
        return self

    def get_present_product_elements(self, num_product=0):
        self._scroll_until_all_product_present(num_product)
        elem_list = self.find_present_elements(self.product_titles_locator)
        return elem_list

    def _scroll_until_all_product_present(self, num_products):
        current_present_products = self.find_present_elements(self.product_titles_locator)
        while len(current_present_products) < num_products:
            self.scroll_to_bottom()
            current_present_products = self.find_present_elements(self.product_titles_locator)

    def click_category_btn(self, category):
        self.click_element((By.CSS_SELECTOR, f'a[href="./index.html?category={category}"]'))
        return self
