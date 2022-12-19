import logging

from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC


class ActionUtils:
    def __init__(self, driver):
        self.driver = driver

    def find_present_element(self, locator, timeout=10):
        try:
            elem = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((locator)))
        except TimeoutException:
            return None
        return elem

    def find_present_elements(self, locator, timeout=10):
        try:
            elems = WebDriverWait(self.driver, timeout).until(EC.presence_of_all_elements_located((locator)))
        except TimeoutException:
            return []
        return elems

    def find_clickable_element(self, locator, timeout=10):
        try:
            elem = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((locator)))
        except TimeoutException:
            return None
        return elem

    def click_element(self, locator, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((locator))).click()
            return self
        except TimeoutException:
            return self

    def scroll_to_bottom(self):
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        return self

    def get_local_storage_item(self, key):
        js_script = f'return localStorage.getItem("{key}");'
        return self.driver.execute_script(js_script)

    def set_local_storage_item(self, key, value):
        js_script = f'localStorage.setItem("{key}", "{value}");'
        self.driver.execute_script(js_script)

    def get_alert(self, timeout=10):
        alert = WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
        return alert

    def reload_page(self):
        self.driver.refresh()
        return self

    def get_current_tab_handle(self):
        return self.driver.current_window_handle

    def switch_to_new_tab(self):
        self.driver.switch_to.window(self.driver.window_handles[-1])
        logging.info('The window handle has switched to the new tab.')
        return self

    def switch_to_tab(self, handle):
        self.driver.switch_to.window(handle)
        return self

    def get_current_url(self):
        return self.driver.current_url
