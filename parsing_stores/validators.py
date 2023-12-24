import requests


def check_product_magnit(product):
    if requests.get(product['image_url']).status_code != 200:
        return False
    # elif (
    #     product['price_in_store']['initial_price'] <= 0 and
    #     product['price_in_store']['promo_price'] <= 0
    # ):
    #     return False
    else:
        return True
