import pytest


class TestProductPage:
    results = [
        'success',
        'failed'
    ]

    def test_select_color(self, product_page):
        target_color_elem = product_page.select_random_color()
        assert target_color_elem.get_attribute('class') == 'product__color product__color--selected', \
            'the color selected has not been highlighted.'

    def test_select_size(self, product_page):
        target_size_elem = product_page.select_random_size()
        assert target_size_elem.get_attribute('class') == 'product__size product__size--selected', \
            'the color selected has not been highlighted.'

    def test_quantity_disabled(self, product_page):
        current_qty = product_page.get_current_qty()
        product_page.increase_quantity_by()
        new_qty = product_page.get_current_qty()
        assert current_qty == new_qty, f'Without selecting size first, the quantity should still be {current_qty} but not {new_qty}.'

    def test_increase_quantity(self, product_page):
        product_page.select_random_size()
        product_page.increase_quantity_by(8)
        current_qty = product_page.get_current_qty()
        assert current_qty == 9, f'The current quantity should be 9, but get {current_qty}.'

        product_page.increase_quantity_by(2)
        assert current_qty == 9, f'The current quantity should still be 9, but get {current_qty}.'

    def test_decrease_quantity(self, product_page):
        product_page.select_random_size()
        product_page.increase_quantity_by(8)
        product_page.decrease_quantity_by(8)
        current_qty = product_page.get_current_qty()
        assert current_qty == 1, f'The current quantity should be 1, but get {current_qty}.'

    @pytest.mark.parametrize('result', results)
    def test_add_to_cart(self, product_page, result):
        if result == 'success':
            product_page.select_random_size()
            product_page.add_to_cart()
            alert = product_page.get_alert()
            assert alert.text == '已加入購物車', f'The message should be "已加入購物車", but get "{alert.text}".'
            alert.accept()
            cart_icon_number = product_page.get_cart_icon_number()
            assert cart_icon_number == 1, f'The number of product added to cart should be 1, but get {cart_icon_number}.'
        elif result == 'failed':
            product_page.add_to_cart()
            alert = product_page.get_alert()
            assert alert.text == '請選擇尺寸', f'The message should be "請選擇尺寸", but get "{alert.text}".'
            alert.accept()
