from django.urls import path
from .views import (lottery_list, create_lottery, lottery_detail,
                    lottery_entry, user_lottery_entries, my_lotteries,
                    delete_lottery, edit_lottery)


urlpatterns = [
    path('lotteries/', lottery_list, name='lottery_list'),
    path('add-lottery/', create_lottery, name='add_lottery'),
    path('lottery/<int:pk>/', lottery_detail, name='lottery_detail'),
    path('lottery/<int:pk>/enter', lottery_entry, name='lottery_entry'),
    path('lotteries/entries', user_lottery_entries, name='lottery_entry_list'),
    path('my_lotteries/', my_lotteries, name='users_lotteries'),
    path('lottery/<int:pk>/delete/', delete_lottery, name='delete_lottery'),
    path('lottery/<int:pk>/edit', edit_lottery, name='edit_lottery'),

]
