from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models
from api.auth.mixins import HasPolicy
from .policies import UserPolicy

class UserModel(AbstractUser, HasPolicy):
    name = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=20, null=True)
    avatar = models.FileField(upload_to="uploads/", null=True)
    _policy = UserPolicy


class LazyLoadedUserModel:
    __model = None
    
    @property
    def model(self):
        if not self.__model:
            self.refresh()
        return self.__model
    
    def __call__(self, **kargs):
        return self.model(**kargs)
    
    def __getattr__(self, name):
        return getattr(self.model, name)
    
    def refresh(self):
        self.__model = get_user_model()


User = LazyLoadedUserModel()