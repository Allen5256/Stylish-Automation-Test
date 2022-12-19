import random

from selenium.webdriver.common.by import By

from page_objects import CommonPage
from test_data import domain


class ProductPage(CommonPage):
    def __init__(self, driver, product_id=0):
        super().__init__(driver)
        self.product_id = product_id
        self.url = f'{domain}product.html?id={str(product_id)}'
        self.product_info = {
            'id': product_id,
            'title': '',
            'color': '顏色｜',
            'size': '尺寸｜',
            'qty': 1,
            'price': 'NT.'
        }

        # Element locators
        self.product_title_element_selector = (By.XPATH, '//div[@class="product__title"]')
        self.price_element_selector = (By.XPATH, '//div[@class="product__price"]')
        self.color_selector_locator = (By.XPATH, '//div[@class="product__color-selector"]/child::*')
        self.size_selector_locator = (By.XPATH, '//div[@class="product__size-selector"]/child::*')
        self.qty_elem_locator = (By.XPATH, '//div[@class="product__quantity-value"]')
        self.add_qty_btn_locator = (By.XPATH, '//div[@class="product__quantity-add"]')
        self.minus_qty_btn_locator = (By.XPATH, '//div[@class="product__quantity-minus"]')
        self.add_to_cart_btn_locator = (By.XPATH, '//button[@class="product__add-to-cart-button"]')

    def select_random_color(self):
        color_elems = self.find_present_elements(self.color_selector_locator)
        target_color_elem = random.choice(color_elems)
        target_color_elem.click()
        # Store color information into product_info
        self.product_info['color'] = target_color_elem.get_attribute('data_id')[-6:]  # 'color_code_XXXXXX'
        return target_color_elem

    def select_random_size(self):
        size_elems = self.find_present_elements(self.size_selector_locator)
        target_size_elem = random.choice(size_elems)
        target_size_elem.click()
        size_name = target_size_elem.text
        # Store size information into product_info
        self.product_info['size'] = f'尺寸｜{size_name}'
        return target_size_elem

    def store_product_info_title(self):
        title_elem = self.find_present_element(self.product_title_element_selector)
        self.product_info['title'] = title_elem.text

    def store_product_info_price(self):
        price_elem = self.find_present_element(self.price_element_selector)
        price_str = f'NT.{price_elem.text[4:]}'  # 'TWD.XXXX' -> 'NT.XXXX'
        self.product_info['price'] = price_str

    def get_current_qty(self):
        qty_elem = self.find_present_element(self.qty_elem_locator)
        # Store quantity information into product_info
        self.product_info['qty'] = int(qty_elem.text)
        return int(qty_elem.text)

    def increase_quantity_by(self, num=1):
        add_qty_btn_elem = self.find_clickable_element(self.add_qty_btn_locator)
        for i in range(num):
            add_qty_btn_elem.click()
        return self

    def decrease_quantity_by(self, num=1):
        minus_qty_btn_elem = self.find_clickable_element(self.minus_qty_btn_locator)
        for i in range(num):
            minus_qty_btn_elem.click()
        return self

    def add_to_cart(self):
        add_to_cart_btn_elem = self.find_clickable_element(self.add_to_cart_btn_locator)
        add_to_cart_btn_elem.click()
        return self
