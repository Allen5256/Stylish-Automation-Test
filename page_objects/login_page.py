from selenium.webdriver.common.by import By

from page_objects import CommonPage
from test_data import domain, login_info_0, login_info_1, login_info_2


class LoginPage(CommonPage):
    def __init__(self, driver):
        super().__init__(driver)
        self.login_url = f'{domain}login.html'
        self.profile_url = f'{domain}profile.html'

        # Element locators
        self.email_input_locator = (By.CSS_SELECTOR, 'input#email')
        self.password_input_locator = (By.CSS_SELECTOR, 'input#pw')
        self.login_btn_locator = (By.CSS_SELECTOR, 'button.login100-form-btn')
        self.logout_btn_locator = (By.CSS_SELECTOR, 'div.profile__content button')

    def login(self, worker, login_info=None):

        def get_login_info_by_worker(id_str):
            # 不另外帶登入資訊進來的話(失敗情境)，就去抓預設好的登入資訊(會登入成功)
            if id_str == 'master' or id_str == 'gw0':
                info = login_info_0
            elif id_str == 'gw1':
                info = login_info_1
            elif id_str == 'gw2':
                info = login_info_2
            return info

        if login_info is None:
            login_info = get_login_info_by_worker(worker)

        # Key in email
        self.find_clickable_element(self.email_input_locator).send_keys(login_info['email'])
        # Key in password
        self.find_clickable_element(self.password_input_locator).send_keys(login_info['password'])
        # Click login button
        self.find_clickable_element(self.login_btn_locator).click()
        return self

    def logout(self):
        self.find_clickable_element(self.logout_btn_locator).click()
        return self

    def head_to_profile_page(self):
        self.driver.get(self.profile_url)
        return self
