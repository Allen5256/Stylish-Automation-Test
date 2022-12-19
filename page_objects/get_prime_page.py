from selenium.webdriver.common.by import By

from page_objects import ActionUtils
from test_data import domain


class GetPrimePage(ActionUtils):
    def __init__(self, driver):
        super().__init__(driver)
        self.url = f'{domain}get_prime.html'

        # Element locators
        self.card_number_iframe = (By.XPATH, '//div[@id="card-number"]/iframe')
        self.card_number_input = (By.XPATH, '//input[@id="cc-number"]')

        self.card_date_iframe = (By.XPATH, '//div[@id="card-expiration-date"]/iframe')
        self.card_date_input = (By.XPATH, '//input[@id="cc-exp"]')

        self.card_ccv_iframe = (By.XPATH, '//div[@id="card-ccv"]/iframe')
        self.card_ccv_input = (By.XPATH, '//input[@id="cc-cvc"]')

        self.get_prime_button = (By.XPATH, '//button[@id="checkoutBtn"]')

    def get_prime(self):
        card_info = {
            'card_number': '4242-4242-4242-4242',
            'car_exp_date': '1223',
            'card_ccv': '123'
        }

        self.driver.switch_to.frame(self.find_present_element(self.card_number_iframe))
        self.find_clickable_element(self.card_number_input).send_keys(card_info['card_number'])
        self.driver.switch_to.default_content()

        self.driver.switch_to.frame(self.find_present_element(self.card_date_iframe))
        self.find_clickable_element(self.card_date_input).send_keys(card_info['car_exp_date'])
        self.driver.switch_to.default_content()

        self.driver.switch_to.frame(self.find_present_element(self.card_ccv_iframe))
        self.find_clickable_element(self.card_ccv_input).send_keys(card_info['card_ccv'])
        self.driver.switch_to.default_content()

        self.find_clickable_element(self.get_prime_button).click()

        alert = self.get_alert()
        prime = alert.text
        alert.accept()

        return prime
