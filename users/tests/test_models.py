from django.test import TestCase
from factories.users import UserFactory


class UserModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory()
        cls.user_without_name = UserFactory(first_name='', last_name='')

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        user = UserModelTest.user
        field_verboses = {
            'username': 'email',
            'phone': 'Телефон',
            'role': 'Роль пользователя приложения',
            'photo': 'Фото пользователя',
            'gender': 'Пол',
            'date_of_birth': 'День рождения'
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    user._meta.get_field(field).verbose_name, expected_value)

    def test_str_user_fullname(self):
        """Выводится полное имя пользователя."""
        user = UserModelTest.user
        self.assertEqual(user.__str__(), self.user.get_full_name())

    def test_str_username(self):
        """Выводится ник пользователя."""
        user = UserModelTest.user_without_name
        self.assertEqual(user.__str__(), self.user_without_name.username)
