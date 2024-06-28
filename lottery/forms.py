from django import forms
from .models import Lottery
from django.core.exceptions import ValidationError
import datetime


class LotteryForm(forms.ModelForm):
    
    class Meta:
        model = Lottery
        fields = ['image', 'creator', 'expiry_date', 'amount_to_enter', 'winning_amount', 'winner']
    
    def clean_creator(self):
        creator = self.cleaned_data.get("creator")
        age = datetime.now().year - creator.birth_date.year
        
        if age < 18:
            raise ValidationError("The User's age is below 18. The Minimum Age required is 18!")
        else:
            return creator
