from http import HTTPStatus

from django.test import Client, TestCase


class PagesURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_urls_exists_at_desired_location_guest(self):
        """Страницы 'api/products/, api/products/1/, api/categories/, api/stores/' доступны любому пользователю."""
        url_names = (
            '/',
            '/api/products/',
            'api/products/1/',
            '/api/categories/',
            '/api/stores/'
        )
        for address in url_names:
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_unexisting(self):
        """Несуществующая страница выдаёт код 404."""
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
