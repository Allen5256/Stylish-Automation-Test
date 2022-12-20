import random

import pytest
import allure

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from database_utils import SQLObject
from page_objects import *
from test_data import *


@pytest.fixture(name='driver')
def init_webdriver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.set_window_size(1920, 1080)
    yield driver
    allure.attach(driver.get_screenshot_as_png())
    driver.quit()


@pytest.fixture(name='login_driver')
def get_login_driver(driver, worker_id):
    page_obj = LoginPage(driver)
    driver.get(page_obj.login_url)
    page_obj.login(worker_id)
    page_obj.get_alert().accept()
    yield driver


@pytest.fixture(name='product_page')
def head_to_product_page(driver, products_info):
    product_id = random.choice(products_info.index)
    page_obj = ProductPage(driver, product_id)
    driver.get(page_obj.url)
    yield page_obj


@pytest.fixture(name='create_page')
def head_to_create_page(driver):
    page_obj = AdminPage(driver)
    driver.get(page_obj.create_url)
    yield page_obj


@pytest.fixture(name='products_info')
def get_all_product_names_with_category():
    sql_obj = SQLObject(db_settings)
    target_cols = ('id', 'title', 'category')
    target_table = 'product'
    info_df = sql_obj.select_data_as_df(target_cols, target_table, index_col='id')
    yield info_df
    sql_obj.disconnect()


@pytest.fixture(name='color_conversion')
def get_color_code_conversion():
    sql_obj = SQLObject(db_settings)
    target_cols = ('code', 'name')
    target_table = 'color'
    info_df = sql_obj.select_data_as_df(target_cols, target_table, index_col='code')
    yield info_df
    sql_obj.disconnect()
