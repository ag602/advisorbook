from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    name = models.CharField(_('Full Name'), max_length=30, blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True, primary_key=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    booking_time = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Advisor(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    photo_url = models.CharField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='userr', blank=True, null=True)
    advisor = models.ForeignKey(Advisor, on_delete=models.CASCADE, related_name='advisorr', blank=True, null=True)
    booking_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'User - %s | Advisor - %s' % (self.user, self.advisor)
