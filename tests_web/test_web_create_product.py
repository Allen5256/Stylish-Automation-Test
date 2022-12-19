import pytest

from page_objects import init_page_objects, LoginPage
from test_data import *

excel_name = 'Stylish-Test Case.xlsx'
success_sheet_name = 'Create Product Success'
failed_sheet_name = 'Create Product Failed'


class TestCreateProduct:
    @pytest.mark.parametrize('test_data', get_row_data(excel_name, success_sheet_name))
    def test_create_product_success(self, login_driver, test_data):
        init_page_objects(login_driver)
        admin_page = login_driver.admin_page_object
        login_driver.get(admin_page.admin_url)
        admin_page_handle = admin_page.get_current_tab_handle()

        admin_page.open_create_page()
        create_page = admin_page.switch_to_new_tab()

        # Pre-process abnormal data
        row = preprocess_data_in_row(test_data)

        alert = create_page.fill_in_product_data(row).click_create_btn().get_alert()
        assert alert.text == 'Create Product Success', \
            f'The alert message should be "Create Product Success", but get "{alert.text}".'
        alert.accept()
        # The tab will close automatically after alert popup is checked.

        admin_page = create_page.switch_to_tab(admin_page_handle)
        admin_page.reload_page()
        admin_page.delete_product()

    @pytest.mark.parametrize('test_data', get_row_data(excel_name, failed_sheet_name))
    def test_create_product_failed(self, login_driver, test_data):
        init_page_objects(login_driver)
        admin_page = login_driver.admin_page_object
        login_driver.get(admin_page.admin_url)
        admin_page_handle = admin_page.get_current_tab_handle()

        admin_page.open_create_page()
        create_page = admin_page.switch_to_new_tab()

        # Pre-process abnormal data
        row = preprocess_data_in_row(test_data)

        alert = create_page.fill_in_product_data(row).click_create_btn().get_alert()
        assert alert.text == row['Alert Msg'], \
            f'The alert message should be "{row["Alert Msg"]}", but get "{alert.text}".'
        alert.accept()
        # The tab will close automatically after alert popup is checked.

        admin_page = create_page.switch_to_tab(admin_page_handle)
        admin_page.reload_page()
        admin_page.delete_product()

    @pytest.mark.parametrize('row', get_row_data(excel_name, success_sheet_name))
    def test_create_product_without_login(self, create_page, row):
        for index, value in row.items():
            if 'chars' in value:
                num_chars = int(value.replace(' chars', ''))
                if num_chars == 1:
                    row = row.replace([value], 'C')
                name_str = 'allenlee'
                multi = num_chars // len(name_str)
                remain = num_chars % len(name_str)
                new_data_str = name_str * multi + name_str[:remain]
                row = row.replace([value], new_data_str)
            elif index == 'Title':
                row = row.replace([value], 'allenlee_' + value)

        alert = create_page.fill_in_product_data(row).click_create_btn().get_alert()
        assert alert.text == 'Please Login First', \
            f'The alert message should be "Please Login First", but get "{alert.text}".'
        alert.accept()
        # The tab should head to login page automatically after alert popup is checked.

        exp_login_page = LoginPage(create_page.driver)
        assert exp_login_page.get_current_url() == exp_login_page.login_url, \
            f'Expected current url should be "{exp_login_page.login_url}", but get "{exp_login_page.get_current_url()}".'
