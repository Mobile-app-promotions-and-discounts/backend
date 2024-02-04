from typing import List, Dict, Tuple

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404

from parsing_stores.magnit.async_magnit_parsing import run_get_data_in_stores
from products.models import Product, Category, Discount, ProductsInStore, Store
from parsing_stores.magnit.decorators import calc_time_work


def create_products_obj(data: List[Dict[str, str | bytes | None]]) -> List[Product]:
    """Создание объектов продукта."""
    return [
        Product(
            category=Category.objects.get(name=product.pop('category')),
            **product,
        ) for product in data
    ]


@calc_time_work
def create_products_and_discounts_obj(data: List[Dict[str, str | bytes | None]]) -> Tuple[List[Product], List[Discount]]:
    """Создание списков объектов продуктов и скидок."""
    products = []
    discounts = []
    for item in data:
        # print(item.get('category'))
        category = Category.objects.get(name=item.get('category'))
        name = item.get('name')
        if not Product.objects.filter(name=name).exists():
            product = Product(
                name=name,
                category=category,
                barcode=item.get('barcode'),
                main_image=ContentFile(item.get('image'), name=item.get('image_name')),
            )
            if product not in products:
                products.append(product)
        discount_rate = item.get('discount_rate') if item.get('discount_rate') else -1
        discount_start = item.get('discount_start')
        discount_end = item.get('discount_end')
        if not Discount.objects.filter(discount_rate=discount_rate, discount_start=discount_start, discount_end=discount_end).exists():
            discount = Discount(
                discount_rate=discount_rate,
                discount_start=discount_start,
                discount_end=discount_end,
            )
            discounts.append(discount)
    return products, discounts


def create_products_in_stores_obj(data: List[Dict[str, str | bytes | None]]) -> List[ProductsInStore]:
    """Создание объектов продуктов в магазинах."""
    products_in_stores = []
    for item in data:
        product = get_object_or_404(Product, name=item.get('name'))
        store = Store.objects.get(id_in_chain_store=item.get('id_in_chain_store'))
        discount = Discount.objects.get(
            discount_rate=item.get('discount_rate'),
            discount_start=item.get('discount_start'),
            discount_end=item.get('discount_end'),
        )
        initial_price = item.get('initial_price', False)
        promo_price = item.get('promo_price', False)
        if initial_price and promo_price:
            products_in_stores.append(
                ProductsInStore(
                    product=product,
                    store=store,
                    discount=discount,
                    initial_price=initial_price,
                    promo_price=promo_price,
                )
            )
    return products_in_stores


@calc_time_work
def add_in_db(products: List[Product], discounts: List[Discount]):
    """Добавление данных в БД."""
    add_products = Product.objects.bulk_create(products)
    add_discounts = Discount.objects.bulk_create(discounts)
    # add_products_in_store = ProductsInStore.objects.bulk_create(products_in_stores)
    return add_products, add_discounts


@calc_time_work
def run_add_data_in_db():
    data_in_stores = run_get_data_in_stores()
    products, discounts = create_products_and_discounts_obj(data_in_stores)
    add_products, add_discounts = add_in_db(products, discounts)
    products_in_stores = create_products_in_stores_obj(data_in_stores)
    add_pr_in_stores = ProductsInStore.objects.bulk_create(products_in_stores)
    print(f'Добавлено продуктов {len(add_products)}\nДобавлено акций {len(add_discounts)}\nДобавлено продуктов в магазине {len(add_pr_in_stores)}')
    
