from http import HTTPStatus

from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from factories.products import (CategoryFactory, ProductFactory, ReviewFactory,
                                StoreFactory)
from factories.users import UserFactory
from products.models import Product

FIRST_CATEGORY_BY_PRIORITY = 'Продукты'
# FIXME: временно не отдаем на фронт категорию 'Разное', поэтому в качестве количества категорий указано 8
CATEGORIES_COUNT = 8
PRODUCTS_URL = reverse('api:products-list')
PRODUCT_DETAIL_URL = 'api:products-detail'
CATEGORIES_URL = reverse('api:categories-list')
REVIEWS_URL = 'api:reviews-list'
STORE_PRODUCTS_URL = 'api:store-products-list'
STORES_URL = reverse('api:stores-list')
STORE_CHAINS_URL = reverse('api:chains-list')


class APIViewsTest(APITestCase):
    def setUp(self):
        self.authorized_client = APIClient()
        self.user = UserFactory()
        self.authorized_client.force_authenticate(self.user)
        self.authorized_client_2 = APIClient()
        self.user_2 = UserFactory()
        self.authorized_client_2.force_login(self.user_2)
        self.product = ProductFactory()
        self.store = StoreFactory()
        self.categories = CategoryFactory.create_batch(CATEGORIES_COUNT)
        self.review = ReviewFactory(product=self.product, user=self.user_2)
        self.REVIEWS_URL = reverse(REVIEWS_URL, args=[self.product.id])
        self.STORE_PRODUCTS_URL = reverse(STORE_PRODUCTS_URL, args=[self.store.id])
        self.PRODUCT_DETAIL_URL = reverse(PRODUCT_DETAIL_URL, args=[self.product.id])

    def test_get_all_categories(self):
        response = self.authorized_client.get(CATEGORIES_URL)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.data), len(self.categories))

    def test_get_one_product(self):
        response = self.authorized_client.get(self.PRODUCT_DETAIL_URL)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIsNotNone(response.data.get('id'))
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(response.data.get('id'), self.product.id)
        self.assertEqual(response.data.get('name'), self.product.name)

    def test_category_sorting_by_name(self):
        response = self.authorized_client.get(CATEGORIES_URL)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data[0].get('get_name_display'), FIRST_CATEGORY_BY_PRIORITY)


class PaginatorViewsTest(APITestCase):
    def setUp(self):
        self.authorized_client = APIClient()
        self.user = UserFactory()
        self.authorized_client.force_authenticate(self.user)
        for number in range(1, 24):
            self.product = ProductFactory()
            self.store = StoreFactory()

    def test_first_page_contains_twenty_products(self):
        response = self.authorized_client.get(PRODUCTS_URL)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.data.get('results')), 20)

    def test_second_page_contains_three_products(self):
        response = self.authorized_client.get(PRODUCTS_URL + '?page=2')

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.data.get('results')), 3)

    def test_first_page_contains_twenty_stores(self):
        response = self.authorized_client.get(STORES_URL)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.data.get('results')), 20)

    def test_second_page_contains_three_stores(self):
        response = self.authorized_client.get(STORES_URL + '?page=2')

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.data.get('results')), 3)
