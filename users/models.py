from django.db import models
from django.contrib.auth.models import AbstractUser

from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    required_password_change = models.BooleanField(
        default=False
    )
# The _ is the name of a callable (function, callable object). It's usually used for the gettext function
    password_change_date = models.DateTimeField(
        _('Password change date'), 
        default=timezone.now
    )
