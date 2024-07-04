from django import forms
from .models import User, Wallet
from django.contrib.auth.forms import UserCreationForm


class CustomUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'birth_date', 'user_type']


class WalletForm(forms.ModelForm):
    
    class Meta:
        model = Wallet
        fields = ['user', 'balance']