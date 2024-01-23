import requests


def check_product_magnit(product):
    return not (
        requests.get(product['image_url']).status_code != 200
        or (
            product['price_in_store']['initial_price'] == '-1'
            and product['price_in_store']['promo_price'] == '-1'
        )
    )
