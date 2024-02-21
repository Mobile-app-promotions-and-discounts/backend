from typing import Dict, List, Tuple

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404

from parsing_stores.magnit.async_magnit_parsing import run_get_data_in_stores
from parsing_stores.magnit.decorators import calc_time_work
from parsing_stores.magnit.utils import (get_discount_data, get_product_data,
                                         is_duplicate_in_store,
                                         is_duplicate_product)
from products.models import Category, Discount, Product, ProductsInStore, Store


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
    products_obj = []
    discounts = []
    discounts_obj = []
    for item in data:
        pr = get_product_data(item)
        if not is_duplicate_product(pr, products):
            item['is_duplucate'] = False
            products.append(pr)
        else:
            item['is_duplucate'] = True
        ds = get_discount_data(item)
        if ds not in discounts:
            discounts.append(ds)
    for product_data in products:
        category = Category.objects.get(name=product_data.get('category'))
        name = product_data.get('name')
        if not Product.objects.filter(name=name).exists():
            try:
                product = Product(
                    name=name,
                    category=category,
                    barcode=product_data.get('barcode')[:14],
                    main_image=ContentFile(product_data.get('image'), name=product_data.get('image_name')),
                )
                products_obj.append(product)
            except Exception:
                print(product_data)
    for discount_data in discounts:
        discount_rate = discount_data.get('discount_rate')
        discount_start = discount_data.get('discount_start')
        discount_end = discount_data.get('discount_end')
        if not Discount.objects.filter(discount_rate=discount_rate, discount_start=discount_start, discount_end=discount_end).exists():
            discount = Discount(
                discount_rate=discount_rate,
                discount_start=discount_start,
                discount_end=discount_end,
            )
            discounts_obj.append(discount)
    return products_obj, discounts_obj


def create_products_in_stores_obj(data: List[Dict[str, str | bytes | None]]) -> List[ProductsInStore]:
    """Создание объектов продуктов в магазинах."""
    products_in_stores = []
    data = is_duplicate_in_store(data)
    for item in data:
        if item.get('is_duplicate'):
            continue
        product = Product.objects.filter(
            name=item.get('name'),
            # category__name=item.get('category'),
        ).first()
        store = Store.objects.get(id_in_chain_store=item.get('id_in_chain_store'))
        discount = Discount.objects.get(
            discount_rate=item.get('discount_rate') if item.get('discount_rate') else -1,
            discount_start=item.get('discount_start'),
            discount_end=item.get('discount_end'),
        )
        initial_price = item.get('initial_price', False)
        promo_price = item.get('promo_price', False)
        if (
            (initial_price or promo_price)
            # and not ProductsInStore.objects.filter(
            #     product=product,
            #     store=store,
            #     discount=discount,
            #     initial_price=initial_price,
            #     promo_price=promo_price,
            # ).exists()
        ):
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
    return add_products, add_discounts


@calc_time_work
def run_add_data_in_db():
    data_in_stores = run_get_data_in_stores()
    products, discounts = create_products_and_discounts_obj(data_in_stores)
    add_products, add_discounts = add_in_db(products, discounts)
    # print([item.get('name') for item in data_in_stores if item.get('is_duplicate')])
    products_in_stores = create_products_in_stores_obj(data_in_stores)
    add_pr_in_stores = ProductsInStore.objects.bulk_create(
        products_in_stores,
        # ignore_conflicts=True
        update_conflicts=True,
        update_fields=['initial_price', 'promo_price', 'discount'],
        unique_fields=['product', 'store'],
    )
    print(f'Добавлено продуктов {len(add_products)}\nДобавлено акций {len(add_discounts)}\nДобавлено продуктов в магазине {len(add_pr_in_stores)}')
