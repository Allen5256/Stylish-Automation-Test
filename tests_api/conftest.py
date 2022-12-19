import requests
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from database_utils import SQLObject
from test_data import db_settings, login_info_0, login_info_1, login_info_2
from api_objects import init_api_objects
from page_objects import GetPrimePage


@pytest.fixture(name='session')
def init_api_session():
    session = requests.Session()
    yield session
    session.close()


@pytest.fixture(name='login_session')
def get_session_with_access_token(session, worker_id):
    init_api_objects(session)
    login_api_object = session.login_api_object

    if worker_id == 'master' or worker_id == 'gw0':
        login_info_0['provider'] = 'native'
        login_api_object.set_payload_attribute(**login_info_0)
    elif worker_id == 'gw1':
        login_info_1['provider'] = 'native'
        login_api_object.set_payload_attribute(**login_info_1)
    elif worker_id == 'gw2':
        login_info_2['provider'] = 'native'
        login_api_object.set_payload_attribute(**login_info_2)

    access_token = login_api_object.send_request().get_access_token()

    session.headers['Authorization'] = access_token
    yield session


@pytest.fixture(name='driver')
def init_webdriver():

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    yield driver
    allure.attach(driver.get_screenshot_as_png())
    driver.quit()


@pytest.fixture(name='prime')
def get_prime_from_web(driver):
    get_prime_page = GetPrimePage(driver)
    driver.get(get_prime_page.url)
    prime = get_prime_page.get_prime()
    yield prime


@pytest.fixture(name='db')
def connect_to_database():
    sql_obj = SQLObject(db_settings)
    yield sql_obj
    sql_obj.disconnect()
