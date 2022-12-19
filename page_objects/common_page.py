from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from page_objects import ActionUtils


class CommonPage(ActionUtils):
    def __init__(self, driver):
        super().__init__(driver)

        # Element locators
        self.cart_icon_number_locator = (By.XPATH, '//div[@class="header__link-icon-cart-number"]')

    def get_cart_icon_number(self):
        cart_icon_number_elem = self.find_present_element(self.cart_icon_number_locator)
        return int(cart_icon_number_elem.text)

    def click_shopping_cart_btn(self):
        try:
            self.find_clickable_element((By.CSS_SELECTOR, 'a[href="./cart.html"]')).click()
            return self
        except TimeoutException:
            return self

    def click_profile_btn(self):
        try:
            self.find_clickable_element((By.CSS_SELECTOR, 'a[href="./profile.html"]')).click()
            return self
        except TimeoutException:
            return self
