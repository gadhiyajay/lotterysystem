from django.db import models
from django.contrib.auth.models import AbstractUser
from django_extensions.db.models import TimeStampedModel

# Create your models here.

BUYER = 'buyer'
VENDOR = 'vendor'

USER_TYPES = [
    (BUYER, 'Buyer'),
    (VENDOR, 'Vendor'),
]


class User(AbstractUser):
    user_type = models.CharField(choices=USER_TYPES, default=BUYER, max_length=10)
    birth_date = models.DateField(null=True)
    
    def __str__(self):
        return f'{self.username}'


class Wallet(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return f'{self.user.username}- {self.balance} Rs.'
