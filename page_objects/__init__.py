from .action_utils import ActionUtils
from .common_page import CommonPage
from .home_page import HomePage
from .product_page import ProductPage
from .login_page import LoginPage
from .shopping_cart import ShoppingCart
from .admin_page import AdminPage
from .get_prime_page import GetPrimePage


def init_page_objects(driver):
    driver.home_page_object = HomePage(driver)
    driver.product_page_object = ProductPage(driver)
    driver.login_page_object = LoginPage(driver)
    driver.shopping_cart = ShoppingCart(driver)
    driver.admin_page_object = AdminPage(driver)
    driver.get_prime_page_object = GetPrimePage(driver)
