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
    product_barcode = product.get('barcode')
    for item in products:
        if item.get('name') == product_name or item.get('barcode') == product_barcode:
            print(product_name)
            return True
    return False
