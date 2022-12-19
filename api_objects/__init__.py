from .api_utils import APIUtils
from .user.login_api import LoginAPI
from .user.logout_api import LogoutAPI
from .user.profile_api import ProfileAPI
from .product.get_products_by_category_api import GetProductsByCategoryAPI
from .product.get_products_by_search_api import GetProductsBySearchAPI
from .product.get_products_details_by_id_api import GetProductDetailsByIdAPI
from .order.order_api import OrderAPI
from .order.get_order_by_number_api import GetOrderByNumberAPI


def init_api_objects(session, **kwargs):
    # User group
    session.login_api_object = LoginAPI(session)
    session.logout_api_object = LogoutAPI(session)
    session.profile_api_object = ProfileAPI(session)

    # Product group
    session.get_products_by_category_api_object = GetProductsByCategoryAPI(session, category=kwargs.get('category'))
    session.get_products_by_search_api_object = GetProductsBySearchAPI(session)
    session.get_products_details_by_id_api_object = GetProductDetailsByIdAPI(session)

    # Order group
    session.order_api_object = OrderAPI(session)
    session.get_order_by_number_api_object = GetOrderByNumberAPI(session, order_number=kwargs.get('order_number'))
