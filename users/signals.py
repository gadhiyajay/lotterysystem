from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Wallet


@receiver(post_save, sender=User)
def wallet_automation(sender, instance, created, **kwargs):
    if created and instance.user_type == 'buyer':
        Wallet.objects.create(user=instance)
