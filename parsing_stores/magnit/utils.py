from typing import Dict, List


def get_product_data(data: Dict[str, str]) -> Dict[str, str]:
    """Извлечение данных по продукту."""
    return dict(
        name=data.get('name'),
        barcode=data.get('barcode'), # Здесь будет ломаться если нет штрихкода
        category=data.get('category'),
        image=data.get('image'),
        image_name=data.get('image_name'),
    )


def get_discount_data(data: Dict[str, str]) -> Dict[str, str]:
    """Извлечение данных по акции."""
    return dict(
        discount_rate=data.get('discount_rate') if data.get('discount_rate') else -1,
        discount_start=data.get('discount_start'),
        discount_end=data.get('discount_end'),
    )


def is_duplicate_product(product: Dict[str, str], products: List[Dict[str, str]]) -> bool:
    product_name = product.get('name')
    for item in products:
        if item.get('name') == product_name:
            return True
    return False


def is_duplicate_in_store(products: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Проверка дубликатов продукта в магазине передача всего списка продуктов."""
    products_in_store = []
    for item in products:
        product_name = item.get('name')
        store_id_in_chain = item.get('id_in_chain_store')
        for product in products_in_store:
            if not (
                product.get('name') == product_name
                and product.get('id_in_chain_store') == store_id_in_chain
            ):
                products_in_store.append(i)
    return products_in_store


def is_duplicate_in_store_ii(product, products):
    """Проверка дубликатов продуктов в магазине передача продукта и сортированного списка."""
    product_name = product.get('name')
    store_id_in_chain = product.get('id_in_chain_store')
    for item in products:
        if (
            item.get('name') == product_name
            and item.get('id_in_chain_store') == store_id_in_chain
        ):
            return True
    return False
