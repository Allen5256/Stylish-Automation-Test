import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from page_objects import CommonPage
from test_data import domain


class ShoppingCart(CommonPage):
    def __init__(self, driver):
        super().__init__(driver)
        self.url = f'{domain}cart.html'

        # Cart item info element locators (除了 qty 的 locator 以外，購物車跟訂購完成頁都共用)
        self.items_list_locator = (By.CSS_SELECTOR, 'div.cart__item')
        self.item_name_locator = (By.CSS_SELECTOR, 'div.cart__item-name')
        self.item_id_locator = (By.CSS_SELECTOR, 'div.cart__item-id')
        self.item_color_locator = (By.CSS_SELECTOR, 'div.cart__item-color')
        self.item_size_locator = (By.CSS_SELECTOR, 'div.cart__item-size')
        self.item_qty_locator = (By.CSS_SELECTOR, 'select.cart__item-quantity-selector')
        self.item_price_locator = (By.CSS_SELECTOR, 'div.cart__item-price-content')
        self.item_subtotal_locator = (By.CSS_SELECTOR, 'div.cart__item-subtotal-content')
        self.checkout_btn_locator = (By.CSS_SELECTOR, 'button.checkout-button')
        self.delete_btn_locator = (By.CSS_SELECTOR, 'div.cart__delete-button')

        self.qty_locator_in_thankyou = (By.XPATH, '//div[@class="cart__item-quantity-title"]/following-sibling::div')

        # Checkout input element locators
        self.recipient_name = (By.XPATH, '//div[text()="收件人姓名"]/following-sibling::input')
        self.recipient_email = (By.XPATH, '//div[text()="Email"]/following-sibling::input')
        self.recipient_mobile = (By.XPATH, '//div[text()="手機"]/following-sibling::input')
        self.recipient_address = (By.XPATH, '//div[text()="地址"]/following-sibling::input')
        self.deliver_time = (By.XPATH, '//input[@type="radio"]')

        # Credit card input element locators
        self.card_number_iframe = (By.XPATH, '//*[@id="card-number"]/iframe')
        self.card_number_input = (By.XPATH, '//*[@id="cc-number"]')
        self.card_date_iframe = (By.XPATH, '//*[@id="card-expiration-date"]/iframe')
        self.card_date_input = (By.XPATH, '//*[@id="cc-exp"]')
        self.card_ccv_iframe = (By.XPATH, '//*[@id="card-ccv"]/iframe')
        self.card_ccv_input = (By.XPATH, '//*[@id="cc-ccv"]')

    def get_num_products_in_cart(self):
        item_elements = self.find_present_elements(self.items_list_locator)
        return len(item_elements)

    def get_items_info(self):
        item_name = self.find_present_element(self.item_name_locator)
        item_id = self.find_present_element(self.item_id_locator)
        item_color = self.find_present_element(self.item_color_locator)
        item_size = self.find_present_element(self.item_size_locator)
        item_qty = self.find_present_element(self.item_qty_locator)
        item_price = self.find_present_element(self.item_price_locator)
        item_subtotal = self.find_present_element(self.item_subtotal_locator)

        item_info = {}
        item_info['title'] = item_name.text
        item_info['id'] = int(item_id.text)
        item_info['color'] = item_color.text
        item_info['size'] = item_size.text
        item_info['qty'] = int(Select(item_qty).first_selected_option.text)
        item_info['price'] = item_price.text
        item_info['subtotal'] = int(item_subtotal.text[3:])  # 'NT.XXXX'

        return item_info

    def select_qty(self):
        qty_selector = Select(self.find_clickable_element(self.item_qty_locator))
        available_qty = []
        for option in qty_selector.options:
            available_qty.append(option.text)
        target_qty = random.choice(available_qty)
        qty_selector.select_by_visible_text(target_qty)
        return target_qty

    def delete_product(self):
        self.find_clickable_element(self.delete_btn_locator).click()
        return self

    def checkout(self):
        self.find_clickable_element(self.checkout_btn_locator).click()
        return self

    def fill_in_checkout_values(self, row):
        if 'chars' in row['Receiver']:
            target_num_chars = int(row['Receiver'][:-6])  # 'xxx chars'
            fake_input = 'x' * target_num_chars
            self.find_clickable_element(self.recipient_name).send_keys(fake_input)
        else:
            self.find_clickable_element(self.recipient_name).send_keys(row['Receiver'])

        if 'chars' in row['Email']:
            target_num_chars = int(row['Email'][:-6])  # 'xxx chars'
            fake_input = 'x' * target_num_chars
            self.find_clickable_element(self.recipient_email).send_keys(fake_input)
        else:
            self.find_clickable_element(self.recipient_email).send_keys(row['Email'])

        self.find_clickable_element(self.recipient_mobile).send_keys(row['Mobile'])

        if 'chars' in row['Address']:
            target_num_chars = int(row['Address'][:-6])  # 'xxx chars'
            fake_input = 'x' * target_num_chars
            self.find_clickable_element(self.recipient_address).send_keys(fake_input)
        else:
            self.find_clickable_element(self.recipient_address).send_keys(row['Address'])

        if row['Deliver Time'] == 'Morning':
            self.find_present_elements(self.deliver_time)[0].click()
        elif row['Deliver Time'] == 'Afternoon':
            self.find_present_elements(self.deliver_time)[1].click()
        elif row['Deliver Time'] == 'Anytime':
            self.find_present_elements(self.deliver_time)[2].click()

        self.driver.switch_to.frame(self.find_present_element(self.card_number_iframe))
        self.find_clickable_element(self.card_number_input).send_keys(row['Credit Card No'])
        self.driver.switch_to.default_content()

        self.driver.switch_to.frame(self.find_present_element(self.card_date_iframe))
        self.find_clickable_element(self.card_date_input).send_keys(row['Expiry Date'])
        self.driver.switch_to.default_content()

        self.driver.switch_to.frame(self.find_present_element(self.card_ccv_iframe))
        self.find_clickable_element(self.card_ccv_input).send_keys(row['Security Code'])
        self.driver.switch_to.default_content()

        return self

    def get_thankyou_page_info(self):
        item_name = self.find_present_element(self.item_name_locator)
        item_id = self.find_present_element(self.item_id_locator)
        item_color = self.find_present_element(self.item_color_locator)
        item_size = self.find_present_element(self.item_size_locator)
        item_qty = self.find_present_element(self.qty_locator_in_thankyou)
        item_price = self.find_present_element(self.item_price_locator)
        item_subtotal = self.find_present_element(self.item_subtotal_locator)

        item_info = {}
        item_info['title'] = item_name.text
        item_info['id'] = int(item_id.text)
        item_info['color'] = item_color.text
        item_info['size'] = item_size.text
        item_info['qty'] = int(item_qty.text)
        item_info['price'] = item_price.text
        item_info['subtotal'] = int(item_subtotal.text[3:])  # 'NT.XXXX'

        return item_info
