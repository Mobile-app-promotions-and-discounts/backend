import factory.fuzzy
from django.contrib.auth import get_user_model
from faker import Faker

fake = Faker(locale='ru_RU')

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.LazyAttribute(lambda _: fake.unique.email())
    username = email
    password = factory.PostGenerationMethodCall('set_password', 'pass')
    phone = factory.Faker('phone_number', locale='ru_RU')
    role = factory.fuzzy.FuzzyChoice(User.RoleType.values)
    foto = factory.django.ImageField(
        color=factory.Faker('color'),
        width=factory.Faker('random_int', min=10, max=1000),
        height=factory.SelfAttribute('width'),
    )
