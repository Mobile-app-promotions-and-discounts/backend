from http import HTTPStatus

from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from factories.products import ProductFactory, ReviewFactory, StoreFactory
from factories.users import UserFactory


PRODUCTS_URL = reverse('api:products-list')
CATEGORIES_URL = reverse('api:categories-list')
STORES_URL = reverse('api:stores-list')
STORE_CHAINS_URL = reverse('api:chains-list')


class PagesURLTests(APITestCase):
    def setUp(self):
        self.guest_client = APIClient()
        self.authorized_client = APIClient()
        self.user = UserFactory()
        self.authorized_client.force_authenticate(self.user)
        self.product = ProductFactory()
        self.store = StoreFactory()
        self.review = ReviewFactory(product=self.product, user=self.user)
        self.REVIEWS_URL = reverse('api:reviews-list', args=[self.product.id])
        self.STORE_PRODUCTS_URL = reverse('api:store-products-list', args=[self.store.id])

    def test_authorized_urls_exists_at_desired_location(self):
        """Страницы доступны авторизованному пользователю."""
        url_names = (
            PRODUCTS_URL,
            self.REVIEWS_URL,
            CATEGORIES_URL,
            STORES_URL,
            self.STORE_PRODUCTS_URL,
            STORE_CHAINS_URL
        )

        for address in url_names:
            with self.subTest(address=address):
                response = self.authorized_client.get(address)

                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_forbidden_urls_for_unauthorized_user(self):
        """Страницы не доступны неавторизованному пользователю."""
        url_names = (
            PRODUCTS_URL,
            self.REVIEWS_URL,
            CATEGORIES_URL,
            STORES_URL,
            self.STORE_PRODUCTS_URL,
            STORE_CHAINS_URL
        )

        for address in url_names:
            with self.subTest(address=address):
                response = self.guest_client.get(address)

                self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_unexisting(self):
        """Несуществующая страница выдаёт код 404."""
        response = self.authorized_client.get('/unexisting_page/')

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
