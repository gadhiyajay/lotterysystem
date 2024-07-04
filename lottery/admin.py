from django.contrib import admin
from .models import Lottery, LotteryEntry
# Register your models here.
admin.site.register(Lottery)
admin.site.register(LotteryEntry)
