import factory
from django.contrib.auth.hashers import make_password
from .models import UserModel
from allauth.account.models import EmailAddress


class UserFactory(factory.django.DjangoModelFactory):
    email = factory.Faker('email')
    username = factory.Faker('user_name')
    name = factory.Faker('name')
    plain_password = 'password'
    password = factory.LazyAttribute(lambda o: make_password(o.plain_password))
    
    class Meta:
        model = UserModel
        exclude = ('plain_password',)
        
    class Params:
        has_phone_number = factory.Trait(
            phone_number=factory.Faker('phone_number')
        )
        
    @factory.post_generation
    def setup_email(obj, create, extracted, **kwargs):  
        EmailAddress.objects.create(user=obj, email=obj.email, verified=True, primary=True)