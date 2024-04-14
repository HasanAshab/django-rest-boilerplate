from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from api.common.utils import LazyProxy
from api.authentication.mixins import HasPolicy
from .policies import UserPolicy


class UserModel(AbstractUser, HasPolicy):
    first_name = None
    last_name = None
    #email = models.EmailField(_('Email Address'), unique=True)
    name = models.CharField(_('Name'), max_length=255, null=True)
    phone_number = models.CharField(_('Phone Number'), max_length=20, null=True)
    avatar = models.ImageField(_('Avatar'), upload_to="uploads/avatars/", max_length=100, null=True)
    _policy = UserPolicy

    @property
    def is_email_verified(self):
        return self.emailaddress_set.filter(primary=True, verified=True).exists()
 

User = LazyProxy(get_user_model)