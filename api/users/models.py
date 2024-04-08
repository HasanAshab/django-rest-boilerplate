from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from api.auth.mixins import HasPolicy
from .policies import UserPolicy

class UserModel(AbstractUser, HasPolicy):
    first_name = None
    last_name = None
    email = models.EmailField(_('Email Address'), unique=True)
    is_email_verified = models.BooleanField(default=False)
    name = models.CharField(_('Name'), max_length=255, null=True)
    phone_number = models.CharField(_('Phone Number'), max_length=20, null=True)
    avatar = models.FileField(_('Avatar'), upload_to="uploads/", null=True)
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