from django.core.files.base import ContentFile

from parsing_stores.magnit.async_magnit_parsing import run_get_data_in_stores
from products.models import Product, Discount, ProductsInStore, Store, Category
from parsing_stores.magnit.decorators import calc_time_work


@calc_time_work
def run_add_in_db(data):
    pr_count = 0
    disc_count = 0
    pr_in_store_count = 0
    for item in data:
        pr_name = item.get('name')
        category_name = item.get('category')
        pr_barcode = item.get('barcode')
        pr_image = item.get('image')
        pr_im_name = item.get('image_name')
        disc_rate = item.get('discount_rate') if item.get('discount_rate') else -1
        disc_end = item.get('discount_end')
        disc_start = item.get('discount_start')
        id_store = item.get('id_in_chain_store')
        init_price = item.get('initial_price')
        promo_price = item.get('promo_price')
        if init_price or promo_price:
            if not Product.objects.filter(name=pr_name).exists():
                category = Category.objects.filter(name=category_name).first()
                product = Product.objects.create(
                    name=pr_name,
                    barcode=pr_barcode,
                    category=category,
                    main_image=ContentFile(pr_image, name=pr_im_name) if pr_image else None,
                )
                pr_count += 1
            else:
                product = Product.objects.filter(name=pr_name).first()
            if not Discount.objects.filter(
                discount_rate=disc_rate,
                discount_start=disc_start,
                discount_end=disc_end,
            ).exists():
                discount = Discount.objects.create(
                    discount_rate=disc_rate,
                    discount_start=disc_start,
                    discount_end=disc_end,
                )
                disc_count += 1
            else:
                discount = Discount.objects.filter(
                                discount_rate=disc_rate,
                                discount_start=disc_start,
                                discount_end=disc_end,
                            ).first()
            store = Store.objects.filter(id_in_chain_store=id_store).first()
            if not ProductsInStore.objects.filter(
                product=product,
                store=store,
            ).exists():
                prod_in_store = ProductsInStore.objects.create(
                    product=product,
                    store=store,
                    initial_price=init_price if init_price else '',
                    promo_price=promo_price if promo_price else '',
                    discount=discount
                )
                pr_in_store_count += 1
    print(f'Добавлено:\n товаров-{pr_count}\nакций-{disc_count}\nтоваров в магазине-{pr_in_store_count}')


def run():
    data = run_get_data_in_stores()
    run_add_in_db(data)
