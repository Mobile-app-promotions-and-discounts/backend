from typing import List, Dict

from parsing_stores.magnit.async_magnit_parsing import run_get_data_in_stores
from products.models import Product, Category, Discount, ProductsInStore, Store


PRODUCT_INDEX = 0
DISCOUNT_INDEX = 1
PRICE_INDEX = 2
STORE_INDEX = 3


def create_products_obj(data: List[Dict[str, str | bytes | None]]) -> List[Product]:
    """Создание объектов продукта."""
    return [
        Product(
            category=Category.objects.get(name=product.pop('category')),
            **product,
        ) for product in data
    ]


def create_discounts_obj(data: List[Dict[str, str]]) -> List[Discount]:
    """Создание объектов скидки."""
    return [Discount(**discount) for discount in data]


def create_products_in_store_obj(data: List[Dict[str, str]]) -> List[ProductsInStore]:
    pass


def split_data(data: List[List[Dict[str, str | bytes | None], Dict[str, str], Dict[str, str]]]) -> List[Dict, Dict, Dict]:
    products_data = []
    discounts_data = []
    products_in_store_data = []
    for item in data:
        category = Category.objects.get(name=item[PRODUCT_INDEX].pop('category'))
        item[PRODUCT_INDEX]['category'] = category
        products_data.append(item[PRODUCT_INDEX])
        discounts_data.append(item[DISCOUNT_INDEX])
        

