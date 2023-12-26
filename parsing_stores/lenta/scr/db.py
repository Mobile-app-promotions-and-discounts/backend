def scr_products_discount(products_discount, name_cat_bd):
    """Получить необходимые данные продуктов."""
    prodacts_data = []

    for value in products_discount:
        products_in_store = {
            'product': {
                'name': value.get('title'),
                'description': (value.get('description')
                                .replace('\r', '').replace('\n', '')),
                'barcode': value.get('code'),
                'category': name_cat_bd,
            },
            'base_price': int(value.get('regularPrice') * 100),
            'sale_price': int(value.get('discountPrice') * 100),
            'discount': {
                'discount_rate': value.get('promoPercent'),
                'discount_start': value.get('validityStartDate')[:10],
                'discount_end': value.get('validityEndDate')[:10],
                'discount_card': cfg.LENTA_VALUE
            }
        }
        if value.get('image'):
            products_in_store['product']['main_image'] = [
                value.get('image').get('fullSize'),
                *[i.get('fullSize') for i in value.get('images')]
            ]
        else:
            products_in_store['product']['main_image'] = None
        prodacts_data.append(products_in_store)
    logger.debug('scr_products_discount - OK')
    return prodacts_data








