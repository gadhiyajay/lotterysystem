from django import forms
from .models import Lottery
from django.core.exceptions import ValidationError
from datetime import date


class LotteryForm(forms.ModelForm):
    class Meta:
        model = Lottery
        fields = ['title', 'description', 'image', 'creator', 'expiry_date', 'amount_to_enter', 'winning_amount',
                  'winner']
        exclude = ['creator', 'winner']

    def clean_creator(self):
        creator = self.cleaned_data.get("creator")

        if not creator.birth_date:
            raise ValidationError("Creator's birth date is not set.")
        today = date.today()
        birth_date = creator.birth_date
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

        if age < 18:
            raise ValidationError("The User's age is below 18. The Minimum Age required is 18!")
        return creator
