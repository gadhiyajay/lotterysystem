from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import User, Wallet, WalletHistory
from decimal import Decimal


@receiver(post_save, sender=User)
def wallet_automation(sender, instance, created, **kwargs):
    if created and instance.user_type == 'buyer':
        Wallet.objects.create(user=instance)


@receiver(pre_save, sender=Wallet)
def wallet_history_update(sender, instance, **kwargs):
    print('Arguments : ', kwargs)
    old_wallet = sender.objects.get(pk=instance.pk)
    if old_wallet:
        old_balance = Decimal(old_wallet.balance)
        new_balance = Decimal(instance.balance)

        if new_balance != old_balance:
            if new_balance > old_balance:
                transaction_type = WalletHistory.CREDIT
                amount = new_balance - old_balance
            else:
                transaction_type = WalletHistory.DEBIT
                amount = old_balance - new_balance

            wallet_history = WalletHistory.objects.create(
                wallet=instance,
                amount=amount,
                transaction_type=transaction_type
            )
            print(f'{wallet_history}')

