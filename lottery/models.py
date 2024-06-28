from django.db import models
from users.models import User
from django_extensions.db.models import TitleDescriptionModel
# Create your models here.


class Lottery(TitleDescriptionModel):
    image = models.ImageField(upload_to='')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by')
    expiry_date = models.DateTimeField()
    amount_to_enter = models.DecimalField(max_digits=10, decimal_places=2)
    winning_amount = models.DecimalField(max_digits=10, decimal_places=2)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_by')

    def __str__(self):
        return f'{self.title} - {self.winner}'
    
    class Meta:
        verbose_name_plural = 'Lotteries'
