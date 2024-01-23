from django.test import TestCase

from factories.products import CategoryFactory, ProductsInStoreFactory


class ProductModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_in_store = ProductsInStoreFactory()

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        product = ProductModelTest.product_in_store.product
        field_verboses = {
            'name': 'Название',
            'description': 'Описание',
            'barcode': 'Штрихкод',
            'category': 'Категория',
            'main_image': 'Главное изображение продукта',
            'stores': 'Магазин',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(product._meta.get_field(field).verbose_name, expected_value)


class CategoryModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = CategoryFactory()

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        category = CategoryModelTest.category
        field_verboses = {
            'name': 'Название',
            'image': 'Иконка категории',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(category._meta.get_field(field).verbose_name, expected_value)
