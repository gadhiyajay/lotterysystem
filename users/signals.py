from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from .models import User, Wallet, WalletHistory
from decimal import Decimal
from lottery.models import LotteryEntry, Lottery
from django.core.exceptions import ValidationError
from django.core.mail import send_mail


@receiver(post_save, sender=User)
def wallet_automation(sender, instance, created, **kwargs):
    if created and instance.user_type == 'buyer':
        Wallet.objects.create(user=instance)


@receiver(pre_save, sender=Wallet)
def wallet_history_update(sender, instance, **kwargs):
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

            WalletHistory.objects.create(
                wallet=instance,
                amount=amount,
                transaction_type=transaction_type
            )


@receiver(pre_save, sender=LotteryEntry)
def wallet_deduction(sender, instance, **kwargs):
    if instance.pk is None:  # navo object check kare!
        user = instance.user
        lottery = instance.lottery
        wallet = Wallet.objects.get(user=user) # we use wallet.objects..... because the lotteryentry model don't have a wallet field!

        entry_fees = Decimal(lottery.amount_to_enter)
        # user wallet insufficient balance check here!
        if wallet.balance < entry_fees:
            raise ValidationError('Insufficient Funds!, To enter into the lottery please add money to the wallet!')
        wallet.balance -= entry_fees
        wallet.save()

        WalletHistory.objects.create(
                wallet=wallet,
                amount=entry_fees,
                transaction_type=WalletHistory.DEBIT
            )


@receiver(pre_delete, sender=Lottery)
def lottery_deletion(sender, instance, **kwargs):
    entries = LotteryEntry.objects.filter(lottery=instance)

    for entry in entries:
        user = entry.user
        wallet = Wallet.objects.get(user=user)
        wallet.balance += instance.amount_to_enter
        wallet.save()

        WalletHistory.objects.create(
            wallet=wallet,
            amount=instance.amount_to_enter,
            transaction_type=WalletHistory.CREDIT
        )

        send_mail(
            subject='Cancellation of Lottery',
            message=f'Dear {user.username}, the lottery "{instance.title}" has been cancelled!, The entry fees have been refunded to your wallet!',
            from_email='jay.gadhiya@trootech.com',
            recipient_list=[user.email]
        )


@receiver(post_save, sender=Lottery)
def lottery_edit(sender, instance, created, **kwargs):
    if not created:
        entries = LotteryEntry.objects.filter(lottery=instance)

        for entry in entries:

           user = entry.user

           send_mail(
               subject=f'Update in Lottery : {instance.title} ',
               message=f'Dear {user.username}, This is to inform you that some changes have been made in the lottery {instance.title}, in which you are enrolled, Please check the updated stats!',
               from_email='jay.gadhiya@trootech.com',
               recipient_list=[user.email]
           )