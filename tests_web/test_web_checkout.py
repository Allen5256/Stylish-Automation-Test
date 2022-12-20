import random

import pytest
from page_objects import ProductPage, ShoppingCart

from test_data import *

excel_name = 'Stylish-Test Case.xlsx'
invalid_sheet_name = 'Checkout with Invalid Value'
valid_sheet_name = 'Checkout with Valid Value'


class TestCheckout:
    def test_empty_cart(self, login_driver):
        shopping_cart = ShoppingCart(login_driver)
        login_driver.get(shopping_cart.url)

        shopping_cart.checkout()
        alert = shopping_cart.get_alert()
        assert alert.text == '尚未選購商品', f'The alert message should be "尚未選購商品", but get "{alert.text}".'
        alert.accept()

    @pytest.mark.parametrize('row', get_row_data(excel_name, invalid_sheet_name))
    def test_checkout_with_invalid_value(self, login_driver, products_info, color_conversion, row):
        # Initial product page object
        product_id = random.choice(products_info.index)
        product_page = ProductPage(login_driver, product_id)
        login_driver.get(product_page.url)
        # Add a product to shopping cart and head to shopping cart
        product_page.store_product_info_title()
        product_page.store_product_info_price()
        product_page.select_random_color()
        product_page.select_random_size()
        product_page.add_to_cart()
        product_page.get_alert().accept()
        product_page.click_shopping_cart_btn()
        product_info = product_page.product_info
        # Replace the color code with its correspond name
        color_name = color_conversion.loc[product_info['color'], 'name']
        product_info['color'] = f'顏色｜{color_name}'

        # Initial shopping cart object
        shopping_cart = ShoppingCart(login_driver)
        shopping_cart.fill_in_checkout_values(row).checkout()
        alert = shopping_cart.get_alert()
        assert alert.text == row['Alert Msg'], f'The alert message should be "{row["Alert Msg"]}", but get "{alert.text}".'
        alert.accept()

    @pytest.mark.parametrize('row', get_row_data(excel_name, valid_sheet_name))
    def test_checkout_with_valid_value(self, login_driver, products_info, color_conversion, row):
        # Initial product page object
        product_id = random.choice(products_info.index)
        product_page = ProductPage(login_driver, product_id)
        login_driver.get(product_page.url)
        # Add a product to shopping cart and head to shopping cart
        product_page.store_product_info_title()
        product_page.store_product_info_price()
        product_page.select_random_color()
        product_page.select_random_size()
        product_page.add_to_cart()
        product_page.get_alert().accept()
        product_page.click_shopping_cart_btn()
        product_info = product_page.product_info
        # Replace the color code with its correspond name
        color_name = color_conversion.loc[product_info['color'], 'name']
        product_info['color'] = f'顏色｜{color_name}'

        # Initial shopping cart object
        shopping_cart = ShoppingCart(login_driver)
        cart_info = shopping_cart.get_items_info()

        shopping_cart.fill_in_checkout_values(row).checkout()
        alert = shopping_cart.get_alert()
        assert alert.text == '付款成功', f'The alert message should be "付款成功", but get "{alert.text}".'
        alert.accept()

        # Verify information in thankyou page
        thankyou_info = shopping_cart.get_thankyou_page_info()
        for key, value in thankyou_info.items():
            assert value == cart_info[key], f'Verifying "{key}": the value is expected to be "{cart_info[key]}", but get "{value}".'
