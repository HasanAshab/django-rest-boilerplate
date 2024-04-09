from django.contrib.auth.hashers import make_password
from factory.django import DjangoModelFactory
from factory import Faker
from .models import UserModel

class UserFactory(DjangoModelFactory):
    class Meta:
        model = UserModel
   
    email = Faker('email')
    is_email_verified = True
    username = Faker('user_name')
    password = make_password('password')
    name = Faker('name')
    # phone_number = Faker('phone_number')
#     avatar = Faker('file_path', extension='jpg')
