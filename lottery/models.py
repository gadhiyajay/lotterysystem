from django.db import models
from users.models import User, Wallet, WalletHistory
from django_extensions.db.models import TitleDescriptionModel
# Create your models here.


class Lottery(TitleDescriptionModel):
    image = models.ImageField(upload_to='')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by')
    expiry_date = models.DateTimeField()
    amount_to_enter = models.DecimalField(max_digits=10, decimal_places=2)
    winning_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.title} - {self.winner}'
    
    class Meta:
        verbose_name_plural = 'Lotteries'


class LotteryEntry(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lottery_entries')
    lottery = models.ForeignKey(Lottery, on_delete=models.CASCADE, related_name='entries')
    entered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} -- {self.lottery.title}'

    class Meta:
        verbose_name_plural = 'Lottery Entries'


class LotteryWinner(models.Model):
    lottery = models.ForeignKey(Lottery, on_delete=models.CASCADE, related_name='winners')


