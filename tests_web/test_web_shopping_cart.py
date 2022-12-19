import random

from page_objects import ProductPage, ShoppingCart
from test_data import *


class TestShoppingCart:
    def test_shopping_cart_info(self, product_page, color_conversion):
        # Add a product to cart and head to shopping cart
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

        # Initial ShoppingCart object
        shopping_cart = ShoppingCart(product_page.driver)
        cart_item_info = shopping_cart.get_items_info()

        for key, value in product_info.items():
            assert cart_item_info[key] == value, \
                f'The {key} value of the product showed in the cart should be: {value}, but get {cart_item_info[key]}.'
        # Calculate the subtotal price
        exp_subtotal = int(cart_item_info['price'][3:]) * cart_item_info['qty']  # The price string looks like 'NT.XXXX'
        assert cart_item_info['subtotal'] == exp_subtotal, \
            f'The subtotal should be {exp_subtotal}, but get {cart_item_info["subtotal"]}.'

    def test_remove_product_from_cart(self, driver, products_info, color_conversion):
        product_id = random.choice(products_info.index)
        product_page = ProductPage(driver, domain, product_id)
        product_page.driver.get(product_page.url)
        product_page.store_product_info_title()
        product_page.store_product_info_price()
        product_page.select_random_color()
        product_page.select_random_size()
        product_page.add_to_cart()
        product_page.get_alert().accept()

        product_id = random.choice(products_info.index)
        product_page = ProductPage(product_page.driver, domain, product_id)
        product_page.driver.get(product_page.url)
        product_page.store_product_info_title()
        product_page.store_product_info_price()
        product_page.select_random_color()
        product_page.select_random_size()
        product_page.add_to_cart()
        product_page.get_alert().accept()

        remain_product_info = product_page.product_info
        # Replace the color code with its correspond name
        color_name = color_conversion.loc[remain_product_info['color'], 'name']
        remain_product_info['color'] = f'顏色｜{color_name}'

        product_page.click_shopping_cart_btn()

        shopping_cart = ShoppingCart(product_page.driver)
        shopping_cart.delete_product()
        alert = shopping_cart.get_alert()
        assert alert.text == '已刪除商品', f'The alert message should be "已刪除商品", but get "{alert.text}".'
        alert.accept()

        cart_item_info = shopping_cart.get_items_info()
        for key, value in remain_product_info.items():
            assert cart_item_info[key] == value, \
                f'The {key} value of the product showed in the cart should be: {value}, but get {cart_item_info[key]}.'
        # Calculate the subtotal price
        exp_subtotal = int(cart_item_info['price'][3:]) * cart_item_info['qty']  # The price string looks like 'NT.XXXX'
        assert cart_item_info['subtotal'] == exp_subtotal, \
            f'The subtotal should be {exp_subtotal}, but get {cart_item_info["subtotal"]}.'

        num_items_in_cart = shopping_cart.get_num_products_in_cart()
        num_items_on_icon = shopping_cart.get_cart_icon_number()
        assert num_items_on_icon == num_items_in_cart, \
            f'There are {num_items_in_cart} in cart, but the number shows on the icon is {num_items_on_icon}.'

    def test_edit_qty(self, product_page):
        # Add a product to cart and head to shopping cart
        product_page.store_product_info_title()
        product_page.store_product_info_price()
        product_page.select_random_color()
        product_page.select_random_size()
        product_page.add_to_cart()
        product_page.get_alert().accept()
        product_page.click_shopping_cart_btn()

        # Initial ShoppingCart object
        shopping_cart = ShoppingCart(product_page.driver)
        shopping_cart.select_qty()

        alert = shopping_cart.get_alert()
        assert alert.text == '已修改數量', f'The alert message should be "已修改數量", but get "{alert.text}".'
        alert.accept()

        cart_item_info = shopping_cart.get_items_info()
        exp_subtotal = int(cart_item_info['price'][3:]) * cart_item_info['qty']  # The price string looks like 'NT.XXXX'
        assert cart_item_info['subtotal'] == exp_subtotal, \
            f'The subtotal should be {exp_subtotal}, but get {cart_item_info["subtotal"]}.'
