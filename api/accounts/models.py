from functools import cached_property
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from .mixins import HasPolicy
from .policies import UserPolicy


class UserModel(AbstractUser, HasPolicy):
    first_name = None
    last_name = None
    email = models.EmailField(_('Email Address'), unique=True)
    is_email_verified = models.BooleanField(default=False)
    name = models.CharField(_('Name'), max_length=255, null=True)
    phone_number = models.CharField(_('Phone Number'), max_length=20, null=True)
    avatar = models.ImageField(_('Avatar'), upload_to="uploads/avatars/", max_length=100, null=True)
    _policy = UserPolicy


class LazyLoadedObj:
    def __init__(self, obj_creator: callable):
        self.create_obj = obj_creator
    
    @cached_property
    def _target_obj(self):
        return self.create_obj()


    def __call__(self, **kargs):
        return self._target_obj(**kargs)
    
    def __getattr__(self, name: str):
        return getattr(self._target_obj, name)
    

User = LazyLoadedObj(get_user_model)