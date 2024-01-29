import asyncio
import json
from time import sleep
from pprint import pprint

# from async_magnit_parsing import main
from decorators import calc_time_work

@calc_time_work
def read_data():
    with open('/home/roman/Dev/cherry_mobile_app/backend/parsing_stores/magnit/products_in_magnit.json', 'r') as file:
        data = json.loads(file.read())
    # print(len(list(data.values())[0]))
    # pprint(list(data.values())[0])
    products_in_stores = []
    products = []
    discounts = []
    prices = []
    for store, data_store in data.items():
        for product, discount, price in data_store:
            products_in_stores.append((product, discount, price, dict(store=store)))
            if product.get('name') not in [pr.get('name') for pr in products]:
                products.append(product)
            if discount not in discounts:
                discounts.append(discount)
            if price not in prices:
                prices.append(price)
    print(len(products))
    pprint(len(discounts))
    pprint(len(prices))
    print(len(products_in_stores))
    pprint(products_in_stores[-1])

read_data()



# @calc_time_work
# def func(a):
#     sleep(1)
#     print(a)


# async def create_or_get_product(data):
#     image_url = data.pop('image_url')
#     name_category = data.pop('category')
#     for key, value in PARSING_MAGNIT.get('CATEGORIES').items():
#         if name_category in value and Category.objects.filter(name=key).exists():
#             category = Category.objects.get(name=key)
#     # КОСТЫЛЬ. если нет такой категории товар попадает в разное.
#     category = category if category else Category.objects.get(name='DIFFERENT')
#     if not Product.objects.filter(**data).exists():
#         # logger.info(f'Добавление продукта в категорию <<{category}>> с данными <<{data}>> в БД')
#         image_name = get_image_name(image_url)
#         image_path = settings.MEDIA_ROOT.joinpath('product_images').joinpath(image_name)
#         if not image_path.exists():
#             with ClientSession() as session:
#                 with session.get(image_url) as result:
#                     image_ = await result.read()
#                     image = ContentFile(image_, name=image_name)
#         else:
#             image = image_path
#         product = Product.objects.create(
#             category=category,
#             main_image=image,
#             **data,
#         )
#     # logger.info(f'Извлечение продукта с данными <<{data}>> из БД')
#     return Product.objects.get(**data)


# if __name__ == '__main__':
#     # func('Hello')
#     result = asyncio.run(main())
