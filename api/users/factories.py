from django.contrib.auth.hashers import make_password
import factory
from factory import Faker
from .models import UserModel

class UserFactory(factory.django.DjangoModelFactory):
    email = Faker('email')
    username = Faker('user_name')
    name = Faker('name')
    plain_password = 'password'
    password = factory.LazyAttribute(lambda o: make_password(o.plain_password))
    
    class Meta:
        model = UserModel
        exclude = ('plain_password',)
        
    class Params:
        has_phone_number = factory.Trait(
            phone_number=Faker('phone_number')
        )