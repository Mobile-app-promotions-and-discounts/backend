from http import HTTPStatus

from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from factories.products import CategoryFactory, ProductFactory, ReviewFactory, StoreFactory
from factories.users import UserFactory
from products.models import Product

FIRST_CATEGORY = 'AUTO'
CATEGORIES_COUNT = 9
PRODUCTS_URL = reverse('api:products-list')
CATEGORIES_URL = reverse('api:categories-list')
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
        self.REVIEWS_URL = reverse('api:reviews-list', args=[self.product.id])
        self.STORE_PRODUCTS_URL = reverse('api:store-products-list', args=[self.store.id])
        self.PRODUCT_DETAIL_URL = reverse('api:products-detail', args=[self.product.id])

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
        self.assertEqual(response.data[0].get('name'), FIRST_CATEGORY)


class PaginatorViewsTest(APITestCase):
    def setUp(self):
        self.authorized_client = APIClient()
        self.user = UserFactory()
        self.authorized_client.force_authenticate(self.user)
        for number in range(1, 14):
            self.product = ProductFactory()
            self.store = StoreFactory()

    def test_first_page_contains_ten_products(self):
        response = self.authorized_client.get(PRODUCTS_URL)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.data.get('results')), 10)

    def test_second_page_contains_three_products(self):
        response = self.authorized_client.get(PRODUCTS_URL + '?page=2')

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.data.get('results')), 3)

    def test_first_page_contains_ten_stores(self):
        response = self.authorized_client.get(STORES_URL)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.data.get('results')), 10)

    def test_second_page_contains_three_stores(self):
        response = self.authorized_client.get(STORES_URL + '?page=2')

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.data.get('results')), 3)